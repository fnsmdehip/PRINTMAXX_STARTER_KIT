'use client';

import { useEffect, useState, useRef, useCallback } from 'react';
import api from '@/lib/api';
import { useToast } from '@/components/Toast';
import { SkeletonList } from '@/components/Skeleton';

interface KBItem {
  id: string;
  title: string;
  content: string;
  type: string;
  createdAt: string;
  updatedAt: string;
}

const TYPE_STYLES: Record<string, { badge: string; label: string }> = {
  faq: { badge: 'badge-blue', label: 'FAQ' },
  page: { badge: 'badge-green', label: 'Page' },
  custom: { badge: 'badge-yellow', label: 'Custom' },
};

export default function KnowledgeBasePage() {
  const toast = useToast();
  const [items, setItems] = useState<KBItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [showBulk, setShowBulk] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [formData, setFormData] = useState({ title: '', content: '', type: 'faq' });
  const [bulkText, setBulkText] = useState('');
  const [saving, setSaving] = useState(false);
  const [dragIdx, setDragIdx] = useState<number | null>(null);
  const [dragOverIdx, setDragOverIdx] = useState<number | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const loadItems = useCallback(() => {
    api
      .getKnowledgeBase()
      .then((data) => setItems(data.items || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    loadItems();
  }, [loadItems]);

  const resetForm = () => {
    setShowForm(false);
    setEditingId(null);
    setFormData({ title: '', content: '', type: 'faq' });
  };

  const handleSave = async () => {
    if (!formData.title.trim() || !formData.content.trim()) {
      toast.warning('Missing Fields', 'Title and content are required.');
      return;
    }
    setSaving(true);
    try {
      if (editingId) {
        await api.updateKnowledgeItem(editingId, formData);
      } else {
        await api.createKnowledgeItem(formData);
      }
      resetForm();
      loadItems();
    } catch {
      // Toast handled by API client
    } finally {
      setSaving(false);
    }
  };

  const handleEdit = (item: KBItem) => {
    setFormData({ title: item.title, content: item.content, type: item.type });
    setEditingId(item.id);
    setShowForm(true);
    setShowBulk(false);
  };

  const handleDelete = async (id: string) => {
    try {
      await api.deleteKnowledgeItem(id);
      loadItems();
    } catch {
      // Toast handled by API client
    }
  };

  const handleBulkImport = async () => {
    if (!bulkText.trim()) {
      toast.warning('Empty Import', 'Paste your FAQ data first.');
      return;
    }

    const lines = bulkText.split('\n').filter((l) => l.trim());
    const parsed: { title: string; content: string; type: string }[] = [];

    for (const line of lines) {
      const parts = line.split('|').map((p) => p.trim());
      if (parts.length >= 2) {
        parsed.push({
          title: parts[0],
          content: parts[1],
          type: parts[2] || 'faq',
        });
      }
    }

    if (parsed.length === 0) {
      toast.error('Invalid Format', 'Use format: Question | Answer (one per line)');
      return;
    }

    setSaving(true);
    try {
      await api.bulkCreateKnowledgeItems(parsed);
      setBulkText('');
      setShowBulk(false);
      loadItems();
    } catch {
      // Toast handled by API client
    } finally {
      setSaving(false);
    }
  };

  const handleCSVUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (evt) => {
      const text = evt.target?.result as string;
      if (text) {
        setBulkText(text.replace(/,/g, ' | ').replace(/"/g, ''));
        setShowBulk(true);
        setShowForm(false);
        toast.info('CSV Loaded', 'Review and edit the data below, then import.');
      }
    };
    reader.readAsText(file);
    e.target.value = '';
  };

  // Drag-to-reorder handlers
  const handleDragStart = (idx: number) => setDragIdx(idx);
  const handleDragOver = (e: React.DragEvent, idx: number) => {
    e.preventDefault();
    setDragOverIdx(idx);
  };
  const handleDrop = (idx: number) => {
    if (dragIdx === null || dragIdx === idx) return;
    const newItems = [...items];
    const [moved] = newItems.splice(dragIdx, 1);
    newItems.splice(idx, 0, moved);
    setItems(newItems);
    setDragIdx(null);
    setDragOverIdx(null);
    toast.info('Reordered', 'Priority order updated locally.');
  };
  const handleDragEnd = () => {
    setDragIdx(null);
    setDragOverIdx(null);
  };

  if (loading) {
    return (
      <div className="space-y-6 max-w-4xl">
        <div className="flex justify-between items-center">
          <div className="skeleton h-5 w-40 rounded" />
          <div className="skeleton h-9 w-28 rounded-lg" />
        </div>
        <SkeletonList rows={4} />
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <p className="text-sm text-gray-400">
            <span className="text-white font-semibold">{items.length}</span> item
            {items.length !== 1 ? 's' : ''} in knowledge base
          </p>
        </div>
        <div className="flex items-center gap-2">
          <input
            ref={fileInputRef}
            type="file"
            accept=".csv,.txt"
            onChange={handleCSVUpload}
            className="hidden"
          />
          <button
            onClick={() => {
              setShowBulk(true);
              setShowForm(false);
            }}
            className="btn-secondary text-xs py-2"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
            </svg>
            Bulk Import
          </button>
          <button
            onClick={() => fileInputRef.current?.click()}
            className="btn-secondary text-xs py-2"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
            </svg>
            Upload CSV
          </button>
          <button
            onClick={() => {
              setShowForm(true);
              setShowBulk(false);
              setEditingId(null);
              setFormData({ title: '', content: '', type: 'faq' });
            }}
            className="btn-primary text-xs py-2"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>
            Add Item
          </button>
        </div>
      </div>

      {/* Bulk Import Panel */}
      {showBulk && (
        <div className="card p-6 space-y-4 animate-scale-in">
          <div className="flex items-center justify-between">
            <h3 className="section-heading text-sm">Bulk Import</h3>
            <button onClick={() => setShowBulk(false)} className="btn-ghost text-xs">
              Cancel
            </button>
          </div>
          <p className="text-xs text-gray-500">
            One item per line. Format: <span className="font-mono text-brand-400">Question | Answer</span>
          </p>
          <textarea
            value={bulkText}
            onChange={(e) => setBulkText(e.target.value)}
            rows={8}
            className="input font-mono text-xs"
            placeholder={`What are your hours? | We're open Monday-Friday, 9am-5pm EST.\nDo you offer free shipping? | Yes, free shipping on orders over $50.\nWhat's your return policy? | 30-day returns on all items.`}
          />
          <div className="flex items-center justify-between">
            <span className="text-xs text-gray-600">
              {bulkText.split('\n').filter((l) => l.includes('|')).length} items detected
            </span>
            <button
              onClick={handleBulkImport}
              disabled={saving}
              className="btn-primary text-xs py-2"
            >
              {saving ? 'Importing...' : 'Import All'}
            </button>
          </div>
        </div>
      )}

      {/* Single Item Form */}
      {showForm && (
        <div className="card p-6 space-y-4 animate-scale-in">
          <div className="flex items-center justify-between">
            <h3 className="section-heading text-sm">
              {editingId ? 'Edit Item' : 'New Knowledge Base Item'}
            </h3>
            <button onClick={resetForm} className="btn-ghost text-xs">
              Cancel
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="label">Type</label>
              <select
                value={formData.type}
                onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                className="input"
              >
                <option value="faq">FAQ</option>
                <option value="page">Website Page</option>
                <option value="custom">Custom Response</option>
              </select>
            </div>
            <div>
              <label className="label">Title / Question</label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                className="input"
              />
            </div>
          </div>

          <div>
            <label className="label">Content / Answer</label>
            <textarea
              value={formData.content}
              onChange={(e) => setFormData({ ...formData, content: e.target.value })}
              rows={5}
              className="input"
            />
          </div>

          <div className="flex gap-2">
            <button
              onClick={handleSave}
              disabled={saving}
              className="btn-primary text-xs py-2"
            >
              {saving ? 'Saving...' : editingId ? 'Update Item' : 'Create Item'}
            </button>
            <button onClick={resetForm} className="btn-secondary text-xs py-2">
              Cancel
            </button>
          </div>
        </div>
      )}

      {/* Items List */}
      {items.length === 0 && !showForm && !showBulk ? (
        <div className="card p-16 text-center">
          <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-surface-50 border border-white/[0.06] flex items-center justify-center">
            <svg className="w-8 h-8 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
            </svg>
          </div>
          <p className="text-sm text-gray-400 font-medium mb-1">No knowledge base items yet</p>
          <p className="text-xs text-gray-600 mb-6">
            Add FAQs, website pages, or custom responses to train your AI agent.
          </p>
          <button
            onClick={() => setShowForm(true)}
            className="btn-primary text-xs py-2"
          >
            Add Your First Item
          </button>
        </div>
      ) : (
        <div className="space-y-2">
          {items.map((item, idx) => (
            <div
              key={item.id}
              draggable
              onDragStart={() => handleDragStart(idx)}
              onDragOver={(e) => handleDragOver(e, idx)}
              onDrop={() => handleDrop(idx)}
              onDragEnd={handleDragEnd}
              className={`card p-4 flex items-start gap-4 group transition-all duration-150 cursor-grab active:cursor-grabbing ${
                dragOverIdx === idx ? 'border-brand-500/40 bg-brand-500/5' : ''
              } ${dragIdx === idx ? 'opacity-50' : ''}`}
            >
              {/* Drag handle */}
              <div className="flex-shrink-0 mt-1 text-gray-700 opacity-0 group-hover:opacity-100 transition-opacity">
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                </svg>
              </div>

              {/* Content */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className={`${TYPE_STYLES[item.type]?.badge || 'badge-gray'} text-[10px]`}>
                    {TYPE_STYLES[item.type]?.label || item.type}
                  </span>
                  <h4 className="text-sm font-medium text-white truncate">{item.title}</h4>
                </div>
                <p className="text-xs text-gray-500 line-clamp-2 leading-relaxed">{item.content}</p>
              </div>

              {/* Actions */}
              <div className="flex gap-1.5 flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                  onClick={() => handleEdit(item)}
                  className="p-1.5 rounded-md text-gray-500 hover:text-brand-400 hover:bg-brand-500/10 transition-colors"
                  title="Edit"
                >
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
                  </svg>
                </button>
                <button
                  onClick={() => handleDelete(item.id)}
                  className="p-1.5 rounded-md text-gray-500 hover:text-danger-400 hover:bg-danger-500/10 transition-colors"
                  title="Delete"
                >
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                  </svg>
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
