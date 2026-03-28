import { templates } from '../templates';
import type { ViewName } from '../types';

interface TemplateLibraryProps {
  navigate: (view: ViewName, templateId?: string) => void;
  isPremium: boolean;
}

const categoryIcons: Record<string, string> = {
  Personal: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z',
  Property: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6',
  Legal: 'M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3',
  Events: 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z',
  Business: 'M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z',
  Media: 'M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z',
};

export default function TemplateLibrary({ navigate, isPremium }: TemplateLibraryProps) {
  const categories = [...new Set(templates.map((t) => t.category))];

  const handleSelect = (templateId: string, isPremiumTemplate: boolean) => {
    if (isPremiumTemplate && !isPremium) {
      navigate('paywall');
    } else {
      navigate('create', templateId);
    }
  };

  return (
    <div className="p-4 md:p-6 max-w-4xl mx-auto">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">Templates</h1>
        <p className="text-gray-400 text-sm mt-1">Choose a template to get started quickly</p>
      </div>

      {categories.map((category) => (
        <div key={category} className="mb-8">
          <div className="flex items-center gap-2 mb-3">
            <svg className="w-5 h-5 text-coral" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d={categoryIcons[category] || categoryIcons.Legal}
              />
            </svg>
            <h2 className="text-lg font-semibold text-white">{category}</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {templates
              .filter((t) => t.category === category)
              .map((template) => (
                <button
                  key={template.id}
                  onClick={() => handleSelect(template.id, template.isPremium)}
                  className="bg-navy-light border border-gray-700 rounded-xl p-4 text-left hover:border-gray-600 active:scale-[0.99] transition-all"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <h3 className="text-white font-medium">{template.name}</h3>
                      <p className="text-gray-400 text-sm mt-1 line-clamp-2">
                        {template.description}
                      </p>
                      <div className="flex items-center gap-2 mt-3">
                        <span className="text-xs text-gray-500">
                          {template.parties.length} parties
                        </span>
                        <span className="text-gray-600">|</span>
                        <span className="text-xs text-gray-500">
                          {template.detailsPrompts.length} fields
                        </span>
                      </div>
                    </div>
                    {template.isPremium && !isPremium && (
                      <span className="ml-3 px-2 py-1 bg-coral/20 text-coral text-xs font-semibold rounded-md flex-shrink-0">
                        PRO
                      </span>
                    )}
                  </div>
                </button>
              ))}
          </div>
        </div>
      ))}

      <button
        onClick={() => navigate('create')}
        className="w-full mt-4 py-4 border-2 border-dashed border-gray-600 rounded-xl text-gray-400 hover:border-gray-500 hover:text-gray-300 transition-colors"
      >
        + Create blank record (no template)
      </button>
    </div>
  );
}
