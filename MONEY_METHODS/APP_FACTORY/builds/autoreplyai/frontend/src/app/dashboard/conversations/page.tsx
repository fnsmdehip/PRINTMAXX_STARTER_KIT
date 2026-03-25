'use client';

import { useEffect, useState, useRef } from 'react';
import api from '@/lib/api';
import { Skeleton } from '@/components/Skeleton';

interface Message {
  id: string;
  content: string;
  role: string;
  timestamp: string;
  responseTimeMs?: number;
}

interface Conversation {
  id: string;
  status: string;
  rating: number | null;
  messageCount: number;
  lastMessage: string;
  createdAt: string;
  updatedAt: string;
  messages: Message[];
}

function formatTime(ts: string) {
  const d = new Date(ts);
  const now = new Date();
  const diffMs = now.getTime() - d.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
}

function formatTimestamp(ts: string) {
  return new Date(ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function ConversationListSkeleton() {
  return (
    <div className="space-y-0 divide-y divide-white/[0.04]">
      {Array.from({ length: 6 }).map((_, i) => (
        <div key={i} className="p-4 space-y-2">
          <Skeleton className="h-4 w-3/4" />
          <div className="flex justify-between">
            <Skeleton className="h-3 w-20" />
            <Skeleton className="h-3 w-16" />
          </div>
        </div>
      ))}
    </div>
  );
}

function MessageBubble({ msg }: { msg: Message }) {
  const isUser = msg.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} animate-fade-in-up`}>
      <div className="max-w-[80%] group">
        {!isUser && (
          <div className="flex items-center gap-2 mb-1.5">
            <div className="w-5 h-5 rounded-full bg-brand-500/20 flex items-center justify-center">
              <svg className="w-3 h-3 text-brand-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <span className="text-[10px] text-gray-600 font-medium uppercase tracking-wider">AI Agent</span>
          </div>
        )}
        <div
          className={`px-4 py-3 rounded-2xl text-sm leading-relaxed ${
            isUser
              ? 'bg-brand-500 text-white rounded-br-md'
              : 'bg-surface-100 text-gray-200 border border-white/[0.06] rounded-bl-md'
          }`}
        >
          {msg.content}
        </div>
        <div
          className={`flex items-center gap-2 mt-1 px-1 ${
            isUser ? 'justify-end' : 'justify-start'
          }`}
        >
          <span className="text-[10px] text-gray-600">{formatTimestamp(msg.timestamp)}</span>
          {msg.responseTimeMs && (
            <span className="text-[10px] text-gray-700 font-mono">{msg.responseTimeMs}ms</span>
          )}
        </div>
      </div>
    </div>
  );
}

export default function ConversationsPage() {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const loadConversations = () => {
    setLoading(true);
    api
      .getConversations(page, search || undefined)
      .then((data) => {
        setConversations(data.conversations || []);
        setTotalPages(data.totalPages || 1);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadConversations();
  }, [page, search]);

  const selected = conversations.find((c) => c.id === selectedId);

  useEffect(() => {
    if (selected) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [selected]);

  return (
    <div className="flex gap-4 h-[calc(100vh-7.5rem)]">
      {/* List panel */}
      <div className="w-80 lg:w-96 flex-shrink-0 flex flex-col card overflow-hidden">
        {/* Search */}
        <div className="p-3 border-b border-white/[0.04]">
          <div className="relative">
            <svg
              className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-600"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
            </svg>
            <input
              type="text"
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setPage(1);
              }}
              className="input pl-10 py-2 text-xs"
              placeholder="Search conversations..."
            />
          </div>
        </div>

        {/* Conversation list */}
        <div className="flex-1 overflow-y-auto">
          {loading ? (
            <ConversationListSkeleton />
          ) : conversations.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full p-6 text-center">
              <svg className="w-10 h-10 text-gray-700 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M20.25 8.511c.884.284 1.5 1.128 1.5 2.097v4.286c0 1.136-.847 2.1-1.98 2.193-.34.027-.68.052-1.02.072v3.091l-3-3c-1.354 0-2.694-.055-4.02-.163a2.115 2.115 0 01-.825-.242m9.345-8.334a2.126 2.126 0 00-.476-.095 48.64 48.64 0 00-8.048 0c-1.131.094-1.976 1.057-1.976 2.192v4.286c0 .837.46 1.58 1.155 1.951m9.345-8.334V6.637c0-1.621-1.152-3.026-2.76-3.235A48.455 48.455 0 0011.25 3c-2.115 0-4.198.137-6.24.402-1.608.209-2.76 1.614-2.76 3.235v6.226c0 1.621 1.152 3.026 2.76 3.235.577.075 1.157.14 1.74.194V21l4.155-4.155" />
              </svg>
              <p className="text-sm text-gray-500">No conversations yet</p>
              <p className="text-xs text-gray-600 mt-1">Conversations will appear once visitors use your widget</p>
            </div>
          ) : (
            conversations.map((conv) => (
              <button
                key={conv.id}
                onClick={() => setSelectedId(conv.id)}
                className={`w-full text-left p-4 border-b border-white/[0.04] transition-colors ${
                  selectedId === conv.id
                    ? 'bg-brand-500/10 border-l-2 border-l-brand-500'
                    : 'hover:bg-white/[0.02] border-l-2 border-l-transparent'
                }`}
              >
                <div className="flex items-start justify-between gap-2 mb-1">
                  <p className="text-sm text-gray-200 truncate flex-1 font-medium">
                    {conv.lastMessage
                      ? conv.lastMessage.slice(0, 50) + (conv.lastMessage.length > 50 ? '...' : '')
                      : 'New conversation'}
                  </p>
                  <span
                    className={`flex-shrink-0 w-2 h-2 rounded-full mt-1.5 ${
                      conv.status === 'active' ? 'bg-success-400' : 'bg-gray-600'
                    }`}
                  />
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-[11px] text-gray-600">
                    {conv.messageCount} msg{conv.messageCount !== 1 ? 's' : ''}
                  </span>
                  <span className="text-[11px] text-gray-600">
                    {formatTime(conv.updatedAt)}
                  </span>
                </div>
                {conv.rating && (
                  <div className="flex items-center gap-0.5 mt-1">
                    {Array.from({ length: 5 }).map((_, i) => (
                      <svg
                        key={i}
                        className={`w-3 h-3 ${i < conv.rating! ? 'text-amber-400' : 'text-gray-700'}`}
                        fill="currentColor"
                        viewBox="0 0 20 20"
                      >
                        <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                      </svg>
                    ))}
                  </div>
                )}
              </button>
            ))
          )}
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="flex items-center justify-between p-3 border-t border-white/[0.04]">
            <button
              onClick={() => setPage(Math.max(1, page - 1))}
              disabled={page <= 1}
              className="btn-ghost text-xs disabled:opacity-30"
            >
              Prev
            </button>
            <span className="text-[11px] text-gray-600 font-mono">
              {page}/{totalPages}
            </span>
            <button
              onClick={() => setPage(Math.min(totalPages, page + 1))}
              disabled={page >= totalPages}
              className="btn-ghost text-xs disabled:opacity-30"
            >
              Next
            </button>
          </div>
        )}
      </div>

      {/* Detail panel */}
      <div className="flex-1 flex flex-col card overflow-hidden min-w-0">
        {selected ? (
          <>
            {/* Header */}
            <div className="flex items-center justify-between px-5 py-3.5 border-b border-white/[0.04] flex-shrink-0">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-surface-50 flex items-center justify-center">
                  <svg className="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                  </svg>
                </div>
                <div>
                  <div className="text-sm text-white font-medium">Visitor Conversation</div>
                  <div className="text-[11px] text-gray-600">
                    Started {new Date(selected.createdAt).toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span
                  className={`badge text-[10px] ${
                    selected.status === 'active' ? 'badge-green' : 'badge-gray'
                  }`}
                >
                  {selected.status}
                </span>
                <span className="badge badge-gray text-[10px]">
                  {selected.messageCount} messages
                </span>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-5 space-y-4">
              {/* Date divider */}
              <div className="flex items-center gap-3 py-2">
                <div className="flex-1 h-px bg-white/[0.04]" />
                <span className="text-[10px] text-gray-600 uppercase tracking-wider">
                  {new Date(selected.createdAt).toLocaleDateString(undefined, { weekday: 'long', month: 'long', day: 'numeric' })}
                </span>
                <div className="flex-1 h-px bg-white/[0.04]" />
              </div>

              {selected.messages.map((msg) => (
                <MessageBubble key={msg.id} msg={msg} />
              ))}
              <div ref={messagesEndRef} />
            </div>
          </>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center text-center p-8">
            <div className="w-16 h-16 rounded-2xl bg-surface-100 border border-white/[0.06] flex items-center justify-center mb-4">
              <svg className="w-8 h-8 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z" />
              </svg>
            </div>
            <p className="text-sm text-gray-400 font-medium">Select a conversation</p>
            <p className="text-xs text-gray-600 mt-1">Choose a conversation from the list to view the full thread</p>
          </div>
        )}
      </div>
    </div>
  );
}
