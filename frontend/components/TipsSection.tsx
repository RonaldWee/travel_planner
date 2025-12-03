'use client';

import { AlertCircle, Shield, Bus, MessageCircle, Banknote } from 'lucide-react';

interface TipsSectionProps {
  tips: any;
}

export default function TipsSection({ tips }: TipsSectionProps) {
  if (!tips || Object.keys(tips).length === 0) {
    return null;
  }

  const sections = [
    {
      key: 'culture_etiquette',
      title: 'Cultural Etiquette',
      icon: MessageCircle,
      color: 'text-blue-600 dark:text-blue-400',
    },
    {
      key: 'safety',
      title: 'Safety Tips',
      icon: Shield,
      color: 'text-green-600 dark:text-green-400',
    },
    {
      key: 'transportation',
      title: 'Transportation',
      icon: Bus,
      color: 'text-purple-600 dark:text-purple-400',
    },
    {
      key: 'money',
      title: 'Money Matters',
      icon: Banknote,
      color: 'text-yellow-600 dark:text-yellow-400',
    },
  ];

  return (
    <div className="card">
      <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
        <AlertCircle className="w-5 h-5" />
        Practical Tips & Advice
      </h3>

      <div className="space-y-6">
        {sections.map((section) => {
          const data = tips[section.key];
          if (!data) return null;

          const Icon = section.icon;

          return (
            <div key={section.key}>
              <h4 className={`text-lg font-semibold mb-3 flex items-center gap-2 ${section.color}`}>
                <Icon className="w-5 h-5" />
                {section.title}
              </h4>

              <div className="bg-gray-50 dark:bg-slate-700 rounded-lg p-4 space-y-2">
                {/* Render tips array */}
                {data.tips && Array.isArray(data.tips) && (
                  <ul className="list-disc list-inside space-y-1 text-sm text-gray-700 dark:text-gray-300">
                    {data.tips.map((tip: string, index: number) => (
                      <li key={index}>{tip}</li>
                    ))}
                  </ul>
                )}

                {/* Render other fields */}
                {Object.entries(data).map(([key, value]) => {
                  if (key === 'tips' || !value) return null;

                  if (typeof value === 'string') {
                    return (
                      <div key={key} className="text-sm">
                        <span className="font-semibold capitalize">{key.replace('_', ' ')}: </span>
                        <span className="text-gray-700 dark:text-gray-300">{value}</span>
                      </div>
                    );
                  }

                  if (typeof value === 'object' && !Array.isArray(value)) {
                    return (
                      <div key={key} className="text-sm">
                        <div className="font-semibold capitalize mb-1">{key.replace('_', ' ')}:</div>
                        <div className="ml-4 space-y-1">
                          {Object.entries(value).map(([subKey, subValue]) => (
                            <div key={subKey}>
                              <span className="text-gray-600 dark:text-gray-400 capitalize">
                                {subKey.replace('_', ' ')}:
                              </span>{' '}
                              <span className="text-gray-700 dark:text-gray-300">
                                {typeof subValue === 'object' ? JSON.stringify(subValue) : String(subValue)}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    );
                  }

                  if (Array.isArray(value)) {
                    return (
                      <div key={key} className="text-sm">
                        <div className="font-semibold capitalize mb-1">{key.replace('_', ' ')}:</div>
                        <ul className="list-disc list-inside ml-4 space-y-1 text-gray-700 dark:text-gray-300">
                          {value.map((item, index) => (
                            <li key={index}>{String(item)}</li>
                          ))}
                        </ul>
                      </div>
                    );
                  }

                  return null;
                })}
              </div>
            </div>
          );
        })}

        {/* General tips */}
        {tips.general_tips && Array.isArray(tips.general_tips) && (
          <div>
            <h4 className="text-lg font-semibold mb-3 text-gray-700 dark:text-gray-300">General Tips</h4>
            <ul className="list-disc list-inside space-y-2 text-sm text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-slate-700 rounded-lg p-4">
              {tips.general_tips.map((tip: string, index: number) => (
                <li key={index}>{tip}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}
