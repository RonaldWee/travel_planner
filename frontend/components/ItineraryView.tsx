'use client';

import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Calendar } from 'lucide-react';

interface ItineraryViewProps {
  itinerary: string;
}

export default function ItineraryView({ itinerary }: ItineraryViewProps) {
  if (!itinerary) {
    return (
      <div className="card">
        <h3 className="text-xl font-semibold mb-4">Itinerary</h3>
        <p className="text-gray-600 dark:text-gray-400">No itinerary available</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
        <Calendar className="w-5 h-5" />
        Your Detailed Itinerary
      </h3>

      <div className="markdown-content">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {itinerary}
        </ReactMarkdown>
      </div>
    </div>
  );
}
