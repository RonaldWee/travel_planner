'use client';

import { useState, useEffect } from 'react';
import { Plane, Calendar, DollarSign, Users } from 'lucide-react';
import { TravelPlanRequest } from '@/lib/api';

interface SearchFormProps {
  onSubmit: (data: TravelPlanRequest) => void;
  isLoading: boolean;
}

export default function SearchForm({ onSubmit, isLoading }: SearchFormProps) {
  const [formData, setFormData] = useState<TravelPlanRequest>({
    destination: '',
    origin: 'SIN',
    departure_date: '',
    return_date: '',
    budget_level: 'moderate',
    interests: [],
    trip_type: 'solo',
    duration_days: 7,
  });

  // Auto-calculate return date when departure date or duration changes
  useEffect(() => {
    if (formData.departure_date && formData.duration_days) {
      const departureDate = new Date(formData.departure_date);
      const returnDate = new Date(departureDate);
      returnDate.setDate(returnDate.getDate() + formData.duration_days);
      
      const returnDateString = returnDate.toISOString().split('T')[0];
      setFormData(prev => ({ ...prev, return_date: returnDateString }));
    }
  }, [formData.departure_date, formData.duration_days]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const interestOptions = [
    'culture', 'food', 'history', 'nature', 'adventure',
    'shopping', 'nightlife', 'beaches', 'architecture', 'museums'
  ];

  return (
    <form onSubmit={handleSubmit} className="card space-y-6">
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
        <Plane className="w-6 h-6" />
        Plan Your Trip
      </h2>

      {/* Destination */}
      <div>
        <label className="label">
          Destination <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          className="input-field"
          placeholder="e.g., Tokyo, Paris, Barcelona"
          value={formData.destination}
          onChange={(e) => setFormData({ ...formData, destination: e.target.value })}
          required
        />
      </div>

      {/* Origin */}
      <div>
        <label className="label">Origin Airport Code</label>
        <input
          type="text"
          className="input-field"
          placeholder="e.g., LAX, JFK, SFO"
          value={formData.origin}
          onChange={(e) => setFormData({ ...formData, origin: e.target.value })}
        />
      </div>

      {/* Departure Date & Duration */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="label flex items-center gap-2">
            <Calendar className="w-4 h-4" />
            Departure Date
          </label>
          <input
            type="date"
            className="input-field"
            value={formData.departure_date}
            onChange={(e) => setFormData({ ...formData, departure_date: e.target.value })}
            min={new Date().toISOString().split('T')[0]}
          />
        </div>

        <div>
          <label className="label">Trip Duration (days)</label>
          <input
            type="number"
            className="input-field"
            min="1"
            max="30"
            value={formData.duration_days}
            onChange={(e) => setFormData({ ...formData, duration_days: parseInt(e.target.value) || 7 })}
          />
        </div>
      </div>

      {/* Return Date (Auto-calculated) */}
      <div>
        <div>
          <label className="label">Return Date (auto-calculated)</label>
          <input
            type="date"
            className="input-field bg-gray-100 dark:bg-gray-700"
            value={formData.return_date}
            readOnly
            disabled
          />
        </div>
      </div>

      {/* Budget Level */}
      <div>
        <label className="label flex items-center gap-2">
          <DollarSign className="w-4 h-4" />
          Budget Level
        </label>
        <select
          className="input-field"
          value={formData.budget_level}
          onChange={(e) => setFormData({ ...formData, budget_level: e.target.value as any })}
        >
          <option value="tight">Tight - Budget Travel</option>
          <option value="moderate">Moderate - Mid-Range</option>
          <option value="flexible">Flexible - Comfortable</option>
        </select>
      </div>

      {/* Trip Type */}
      <div>
        <label className="label flex items-center gap-2">
          <Users className="w-4 h-4" />
          Trip Type
        </label>
        <select
          className="input-field"
          value={formData.trip_type}
          onChange={(e) => setFormData({ ...formData, trip_type: e.target.value as any })}
        >
          <option value="solo">Solo Travel</option>
          <option value="couple">Couple</option>
          <option value="family">Family</option>
          <option value="friends">Friends</option>
        </select>
      </div>

      {/* Interests */}
      <div>
        <label className="label">Interests (select multiple)</label>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-2 mt-2">
          {interestOptions.map((interest) => (
            <label key={interest} className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                className="w-4 h-4 text-primary-600 focus:ring-primary-500"
                checked={formData.interests?.includes(interest)}
                onChange={(e) => {
                  const interests = formData.interests || [];
                  if (e.target.checked) {
                    setFormData({ ...formData, interests: [...interests, interest] });
                  } else {
                    setFormData({ ...formData, interests: interests.filter(i => i !== interest) });
                  }
                }}
              />
              <span className="text-sm text-gray-700 dark:text-gray-300 capitalize">{interest}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isLoading || !formData.destination}
        className="btn-primary w-full py-3 text-lg"
      >
        {isLoading ? (
          <span className="flex items-center justify-center gap-2">
            <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            Creating Your Travel Plan...
          </span>
        ) : (
          'Create Travel Plan'
        )}
      </button>

      {isLoading && (
        <p className="text-sm text-gray-600 dark:text-gray-400 text-center">
          This may take 1-2 minutes as we gather the best information for you...
        </p>
      )}
    </form>
  );
}
