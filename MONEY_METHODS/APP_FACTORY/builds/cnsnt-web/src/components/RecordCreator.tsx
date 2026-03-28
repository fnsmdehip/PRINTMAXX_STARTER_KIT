import { useState, useEffect } from 'react';
import { encrypt } from '../crypto/vault';
import { computeHmac, computeChainHash } from '../crypto/hmac';
import { saveRecord, addAuditEntry, getLastAuditHash, getRecordCount, FREE_RECORD_LIMIT } from '../db/store';
import { getTemplate, templates as allTemplates } from '../templates';
import SignatureCanvas from './SignatureCanvas';
import type { ConsentRecord, Party, Signature, GeoData, ViewName } from '../types';

interface RecordCreatorProps {
  pin: string;
  templateId: string | null;
  navigate: (view: ViewName) => void;
  isPremium: boolean;
}

type Step = 'template' | 'parties' | 'terms' | 'details' | 'signatures' | 'review';

export default function RecordCreator({ pin, templateId, navigate, isPremium }: RecordCreatorProps) {
  const [step, setStep] = useState<Step>(templateId ? 'parties' : 'template');
  const [selectedTemplateId, setSelectedTemplateId] = useState<string | null>(templateId);
  const [title, setTitle] = useState('');
  const [parties, setParties] = useState<Party[]>([{ name: '', role: 'Party A' }, { name: '', role: 'Party B' }]);
  const [terms, setTerms] = useState('');
  const [details, setDetails] = useState<Record<string, string>>({});
  const [signatures, setSignatures] = useState<Signature[]>([]);
  const [signingParty, setSigningParty] = useState<string | null>(null);
  const [geo, setGeo] = useState<GeoData | null>(null);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  const template = selectedTemplateId ? getTemplate(selectedTemplateId) : null;

  useEffect(() => {
    if (template) {
      setTitle(template.name);
      setParties(template.parties.map((p) => ({ name: '', role: p.role })));
      setTerms(template.termsTemplate);
      const detailDefaults: Record<string, string> = {};
      template.detailsPrompts.forEach((prompt) => {
        detailDefaults[prompt] = '';
      });
      setDetails(detailDefaults);
    }
  }, [selectedTemplateId]); // eslint-disable-line react-hooks/exhaustive-deps

  // Get geolocation
  useEffect(() => {
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setGeo({
            latitude: pos.coords.latitude,
            longitude: pos.coords.longitude,
            accuracy: pos.coords.accuracy,
          });
        },
        () => {
          // Geolocation not available or denied - that's fine
        },
        { enableHighAccuracy: true, timeout: 10000 }
      );
    }
  }, []);

  const handleSelectTemplate = (id: string) => {
    setSelectedTemplateId(id);
    setStep('parties');
  };

  const handleSkipTemplate = () => {
    setTitle('');
    setStep('parties');
  };

  const updateParty = (index: number, field: keyof Party, value: string) => {
    setParties((prev) => {
      const updated = [...prev];
      updated[index] = { ...updated[index], [field]: value };
      return updated;
    });
  };

  const addParty = () => {
    setParties((prev) => [...prev, { name: '', role: `Party ${String.fromCharCode(65 + prev.length)}` }]);
  };

  const removeParty = (index: number) => {
    if (parties.length <= 2) return;
    setParties((prev) => prev.filter((_, i) => i !== index));
  };

  const handleSignatureSave = (dataUrl: string) => {
    if (!signingParty) return;
    setSignatures((prev) => [
      ...prev.filter((s) => s.partyName !== signingParty),
      { partyName: signingParty, dataUrl, timestamp: new Date().toISOString() },
    ]);
    setSigningParty(null);
  };

  const handleSave = async () => {
    setSaving(true);
    setError('');

    try {
      // Check free limit
      if (!isPremium) {
        const count = await getRecordCount();
        if (count >= FREE_RECORD_LIMIT) {
          setError('Free limit reached. Upgrade to Pro for unlimited records.');
          setSaving(false);
          return;
        }
      }

      const record: ConsentRecord = {
        id: crypto.randomUUID(),
        templateId: selectedTemplateId,
        title: title || 'Untitled Agreement',
        parties,
        terms,
        details: Object.entries(details)
          .map(([k, v]) => `${k}: ${v}`)
          .join('\n'),
        signatures,
        timestamp: new Date().toISOString(),
        geolocation: geo,
        isPremium: template?.isPremium || false,
      };

      // Encrypt the record
      const plaintext = JSON.stringify(record);
      const { iv, ciphertext, salt } = await encrypt(plaintext, pin);

      // Compute HMAC on ciphertext for integrity
      const hmac = await computeHmac(ciphertext);

      // Save to IndexedDB
      await saveRecord({
        id: record.id,
        iv,
        ciphertext,
        hmac,
        salt,
        createdAt: record.timestamp,
        title: record.title,
      });

      // Audit log
      const prevHash = await getLastAuditHash();
      const auditContent = `create|${record.id}|${record.timestamp}|${record.title}`;
      const hash = await computeChainHash(auditContent, prevHash);
      await addAuditEntry({
        id: crypto.randomUUID(),
        action: 'create',
        recordId: record.id,
        timestamp: record.timestamp,
        details: `Created record: ${record.title}`,
        prevHash,
        hash,
      });

      navigate('dashboard');
    } catch (err) {
      setError('Failed to save record. Please try again.');
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  const canProceed = (s: Step): boolean => {
    switch (s) {
      case 'parties':
        return parties.every((p) => p.name.trim().length > 0) && title.trim().length > 0;
      case 'terms':
        return terms.trim().length > 0;
      case 'details':
        return true; // details are optional
      case 'signatures':
        return signatures.length >= 2 || signatures.length === parties.length;
      default:
        return true;
    }
  };

  const steps: Step[] = template
    ? ['parties', 'terms', 'details', 'signatures', 'review']
    : ['template', 'parties', 'terms', 'details', 'signatures', 'review'];

  const stepIndex = steps.indexOf(step);
  const progress = ((stepIndex + 1) / steps.length) * 100;

  return (
    <div className="p-4 md:p-6 max-w-2xl mx-auto">
      {/* Progress bar */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <button
            onClick={() => {
              if (stepIndex > 0) setStep(steps[stepIndex - 1]);
              else navigate('dashboard');
            }}
            className="text-gray-400 flex items-center gap-1"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back
          </button>
          <span className="text-gray-500 text-sm">
            Step {stepIndex + 1} of {steps.length}
          </span>
        </div>
        <div className="h-1 bg-gray-700 rounded-full overflow-hidden">
          <div
            className="h-full bg-coral rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Step: Template Selection */}
      {step === 'template' && (
        <div>
          <h2 className="text-xl font-bold text-white mb-2">Choose a Template</h2>
          <p className="text-gray-400 text-sm mb-6">Or start from scratch</p>
          <div className="space-y-3 mb-4">
            {allTemplates.filter(t => !t.isPremium || isPremium).map((t) => (
              <button
                key={t.id}
                onClick={() => handleSelectTemplate(t.id)}
                className="w-full bg-navy-light border border-gray-700 rounded-xl p-4 text-left hover:border-gray-600 transition-colors"
              >
                <h3 className="text-white font-medium">{t.name}</h3>
                <p className="text-gray-400 text-sm mt-1">{t.description}</p>
              </button>
            ))}
          </div>
          <button
            onClick={handleSkipTemplate}
            className="w-full py-4 border-2 border-dashed border-gray-600 rounded-xl text-gray-400"
          >
            + Blank record (no template)
          </button>
        </div>
      )}

      {/* Step: Parties */}
      {step === 'parties' && (
        <div>
          <h2 className="text-xl font-bold text-white mb-2">Record Details</h2>
          <p className="text-gray-400 text-sm mb-6">Name the agreement and identify all parties</p>

          <label className="block mb-4">
            <span className="text-gray-300 text-sm font-medium">Agreement Title</span>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. House Guest Waiver - John Smith"
              className="mt-1 w-full bg-navy-light border border-gray-700 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:border-coral focus:outline-none"
            />
          </label>

          <div className="space-y-4">
            {parties.map((party, i) => (
              <div key={i} className="bg-navy-light border border-gray-700 rounded-xl p-4">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-gray-300 text-sm font-medium">{party.role}</span>
                  {parties.length > 2 && (
                    <button onClick={() => removeParty(i)} className="text-red-400 text-xs">
                      Remove
                    </button>
                  )}
                </div>
                <input
                  type="text"
                  value={party.name}
                  onChange={(e) => updateParty(i, 'name', e.target.value)}
                  placeholder={template?.parties[i]?.placeholder || 'Full legal name'}
                  className="w-full bg-navy border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-500 focus:border-coral focus:outline-none mb-2"
                />
                <input
                  type="text"
                  value={party.role}
                  onChange={(e) => updateParty(i, 'role', e.target.value)}
                  placeholder="Role (e.g. Host, Guest)"
                  className="w-full bg-navy border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-500 focus:border-coral focus:outline-none"
                />
              </div>
            ))}
          </div>

          <button
            onClick={addParty}
            className="mt-4 w-full py-3 border border-dashed border-gray-600 rounded-xl text-gray-400 text-sm"
          >
            + Add another party
          </button>

          <button
            onClick={() => setStep('terms')}
            disabled={!canProceed('parties')}
            className={`mt-6 w-full py-3 rounded-xl font-medium transition-colors ${
              canProceed('parties')
                ? 'bg-coral text-white'
                : 'bg-gray-700 text-gray-500 cursor-not-allowed'
            }`}
          >
            Continue
          </button>
        </div>
      )}

      {/* Step: Terms */}
      {step === 'terms' && (
        <div>
          <h2 className="text-xl font-bold text-white mb-2">Terms & Conditions</h2>
          <p className="text-gray-400 text-sm mb-6">
            {template ? 'Review and customize the agreement terms' : 'Enter the terms of your agreement'}
          </p>

          <textarea
            value={terms}
            onChange={(e) => setTerms(e.target.value)}
            rows={16}
            placeholder="Enter the full terms of the agreement here..."
            className="w-full bg-navy-light border border-gray-700 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:border-coral focus:outline-none resize-y text-sm leading-relaxed"
          />

          <button
            onClick={() => setStep('details')}
            disabled={!canProceed('terms')}
            className={`mt-6 w-full py-3 rounded-xl font-medium transition-colors ${
              canProceed('terms')
                ? 'bg-coral text-white'
                : 'bg-gray-700 text-gray-500 cursor-not-allowed'
            }`}
          >
            Continue
          </button>
        </div>
      )}

      {/* Step: Details */}
      {step === 'details' && (
        <div>
          <h2 className="text-xl font-bold text-white mb-2">Additional Details</h2>
          <p className="text-gray-400 text-sm mb-6">Fill in specific details for this agreement</p>

          {template && template.detailsPrompts.length > 0 ? (
            <div className="space-y-4">
              {template.detailsPrompts.map((prompt) => (
                <label key={prompt} className="block">
                  <span className="text-gray-300 text-sm font-medium">{prompt}</span>
                  <input
                    type="text"
                    value={details[prompt] || ''}
                    onChange={(e) => setDetails((prev) => ({ ...prev, [prompt]: e.target.value }))}
                    className="mt-1 w-full bg-navy-light border border-gray-700 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:border-coral focus:outline-none"
                  />
                </label>
              ))}
            </div>
          ) : (
            <textarea
              value={details['notes'] || ''}
              onChange={(e) => setDetails({ notes: e.target.value })}
              rows={6}
              placeholder="Any additional notes or details..."
              className="w-full bg-navy-light border border-gray-700 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:border-coral focus:outline-none resize-y"
            />
          )}

          {geo && (
            <div className="mt-4 bg-ocean/20 border border-ocean/40 rounded-xl p-3 flex items-center gap-3">
              <svg className="w-5 h-5 text-green-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <div>
                <p className="text-green-400 text-xs font-medium">Location captured</p>
                <p className="text-gray-400 text-xs">
                  {geo.latitude.toFixed(4)}, {geo.longitude.toFixed(4)}
                </p>
              </div>
            </div>
          )}

          <button
            onClick={() => setStep('signatures')}
            className="mt-6 w-full py-3 rounded-xl font-medium bg-coral text-white"
          >
            Continue to Signatures
          </button>
        </div>
      )}

      {/* Step: Signatures */}
      {step === 'signatures' && (
        <div>
          <h2 className="text-xl font-bold text-white mb-2">Collect Signatures</h2>
          <p className="text-gray-400 text-sm mb-6">Each party must sign the agreement</p>

          <div className="space-y-3">
            {parties.map((party) => {
              const sig = signatures.find((s) => s.partyName === party.name);
              return (
                <div
                  key={party.name}
                  className="bg-navy-light border border-gray-700 rounded-xl p-4"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-white font-medium">{party.name}</p>
                      <p className="text-gray-400 text-sm">{party.role}</p>
                    </div>
                    {sig ? (
                      <div className="flex items-center gap-2">
                        <svg className="w-5 h-5 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        <span className="text-green-400 text-sm">Signed</span>
                      </div>
                    ) : (
                      <button
                        onClick={() => setSigningParty(party.name)}
                        className="px-4 py-2 bg-coral text-white rounded-lg text-sm font-medium"
                      >
                        Sign
                      </button>
                    )}
                  </div>
                  {sig && (
                    <div className="mt-3 bg-navy rounded-lg p-2">
                      <img src={sig.dataUrl} alt="Signature" className="h-16 mx-auto" />
                      <p className="text-gray-500 text-xs text-center mt-1">
                        Signed at {new Date(sig.timestamp).toLocaleString()}
                      </p>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          <button
            onClick={() => setStep('review')}
            disabled={signatures.length < 2}
            className={`mt-6 w-full py-3 rounded-xl font-medium transition-colors ${
              signatures.length >= 2
                ? 'bg-coral text-white'
                : 'bg-gray-700 text-gray-500 cursor-not-allowed'
            }`}
          >
            {signatures.length >= 2
              ? 'Review Agreement'
              : `Need at least 2 signatures (${signatures.length}/${Math.max(2, parties.length)})`}
          </button>

          {signingParty && (
            <SignatureCanvas
              partyName={signingParty}
              onSave={handleSignatureSave}
              onCancel={() => setSigningParty(null)}
            />
          )}
        </div>
      )}

      {/* Step: Review */}
      {step === 'review' && (
        <div>
          <h2 className="text-xl font-bold text-white mb-2">Review & Save</h2>
          <p className="text-gray-400 text-sm mb-6">Verify all details before encrypting and saving</p>

          <div className="space-y-4">
            <div className="bg-navy-light border border-gray-700 rounded-xl p-4">
              <h3 className="text-coral text-xs font-semibold uppercase tracking-wide mb-2">Title</h3>
              <p className="text-white">{title || 'Untitled Agreement'}</p>
            </div>

            <div className="bg-navy-light border border-gray-700 rounded-xl p-4">
              <h3 className="text-coral text-xs font-semibold uppercase tracking-wide mb-2">Parties</h3>
              {parties.map((p, i) => (
                <p key={i} className="text-white text-sm">
                  {p.role}: <span className="text-gray-300">{p.name}</span>
                </p>
              ))}
            </div>

            <div className="bg-navy-light border border-gray-700 rounded-xl p-4">
              <h3 className="text-coral text-xs font-semibold uppercase tracking-wide mb-2">Signatures</h3>
              <p className="text-white text-sm">{signatures.length} of {parties.length} collected</p>
            </div>

            <div className="bg-navy-light border border-gray-700 rounded-xl p-4">
              <h3 className="text-coral text-xs font-semibold uppercase tracking-wide mb-2">Security</h3>
              <div className="space-y-1">
                <p className="text-green-400 text-sm flex items-center gap-2">
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  AES-256-GCM encryption
                </p>
                <p className="text-green-400 text-sm flex items-center gap-2">
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  HMAC-SHA-256 integrity
                </p>
                <p className="text-green-400 text-sm flex items-center gap-2">
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  Timestamped ({new Date().toLocaleString()})
                </p>
                {geo && (
                  <p className="text-green-400 text-sm flex items-center gap-2">
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    Geolocation stamped
                  </p>
                )}
              </div>
            </div>
          </div>

          {error && (
            <p className="mt-4 text-red-400 text-center text-sm">{error}</p>
          )}

          <button
            onClick={handleSave}
            disabled={saving}
            className="mt-6 w-full py-4 rounded-xl font-medium bg-coral text-white text-lg active:scale-[0.98] transition-transform disabled:opacity-50"
          >
            {saving ? (
              <span className="flex items-center justify-center gap-2">
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Encrypting & Saving...
              </span>
            ) : (
              'Encrypt & Save Record'
            )}
          </button>

          <p className="text-gray-500 text-xs text-center mt-3">
            This record will be encrypted with AES-256-GCM and stored locally on your device.
          </p>
        </div>
      )}
    </div>
  );
}
