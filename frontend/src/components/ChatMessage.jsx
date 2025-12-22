import React from 'react';

const renderTextWithLinks = (text, keyPrefix) => {
  const urlRegex = /(https?:\/\/[^\s]+)/g;
  const parts = text.split(urlRegex);
  return parts.map((part, idx) => {
    if (part.startsWith('http://') || part.startsWith('https://')) {
      return (
        <a
          key={`${keyPrefix}-link-${idx}`}
          href={part}
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-600 underline"
        >
          {part}
        </a>
      );
    }
    return <span key={`${keyPrefix}-text-${idx}`}>{part}</span>;
  });
};

const renderMapEmbed = (url, key) => (
  <div key={key} className="my-2 rounded-lg overflow-hidden border border-gray-200">
    <iframe
      src={url}
      title="map"
      className="w-full h-48"
      loading="lazy"
      referrerPolicy="no-referrer-when-downgrade"
    />
  </div>
);

const formatMessage = (text) => {
  return text.split('\n').map((line, idx) => {
    if (line.startsWith('MAP_EMBED:')) {
      const url = line.replace('MAP_EMBED:', '').trim();
      if (url) {
        return renderMapEmbed(url, `map-${idx}`);
      }
    }
    if (line.startsWith('## ')) {
      return (
        <h3 key={idx} className="font-bold text-sm mt-2 text-gray-800">
          {renderTextWithLinks(line.slice(3), `h-${idx}`)}
        </h3>
      );
    }
    if (line.startsWith('**') && line.endsWith('**')) {
      return <strong key={idx}>{renderTextWithLinks(line.slice(2, -2), `b-${idx}`)}</strong>;
    }
    if (line.startsWith('- ')) {
      return (
        <div key={idx} className="ml-3 text-sm">
          - {renderTextWithLinks(line.slice(2), `li-${idx}`)}
        </div>
      );
    }
    if (/^\d+\.\s/.test(line)) {
      return (
        <div key={idx} className="ml-3 text-sm">
          {renderTextWithLinks(line, `ol-${idx}`)}
        </div>
      );
    }
    return (
      <div key={idx} className="text-sm">
        {line ? renderTextWithLinks(line, `p-${idx}`) : ' '}
      </div>
    );
  });
};

export default function ChatMessage({ message }) {
  const isUser = message.type === 'user';
  const text = message.text || '';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className="w-full max-w-xs">
        <div
          className={`max-w-xs px-4 py-2 rounded-2xl ${
            isUser
              ? 'bg-poly-blue text-white rounded-br-none'
              : 'bg-gray-200 text-gray-900 rounded-bl-none'
          }`}
        >
          <div className="break-words leading-relaxed">
            {isUser ? text : formatMessage(text)}
          </div>
          <span className={`text-xs mt-1 block ${isUser ? 'text-blue-100' : 'text-gray-500'}`}>
            {new Date(message.timestamp).toLocaleTimeString('ko-KR', {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </span>
        </div>
      </div>
    </div>
  );
}
