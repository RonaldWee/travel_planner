# Travel Planner Frontend

Next.js 14 frontend for the AI-powered travel planner.

## Features

- **Search Form**: Intuitive travel planning form with destination, dates, budget, and interests
- **Flight Results**: Display flight options with prices and durations
- **Hotel Results**: Show accommodation options by area and price range
- **Budget Breakdown**: Visual budget estimates for tight, moderate, and flexible spending
- **Attractions**: Categorized attractions with ratings and locations
- **Detailed Itinerary**: Day-by-day markdown itinerary with activities
- **Practical Tips**: Cultural, safety, transportation, and money advice
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Dark Mode**: Automatic dark mode support

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Markdown Rendering**: react-markdown with remark-gfm
- **Icons**: lucide-react

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create `.env.local` from the example:

```bash
cp .env.local.example .env.local
```

Update the API URL if needed:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### 4. Build for Production

```bash
npm run build
npm run start
```

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx           # Root layout with globals
│   ├── page.tsx             # Home page with search form
│   └── plan/
│       └── page.tsx         # Results page with travel plan
├── components/
│   ├── SearchForm.tsx       # Travel planning form
│   ├── FlightList.tsx       # Flight options display
│   ├── HotelList.tsx        # Hotel options display
│   ├── BudgetSummary.tsx    # Budget breakdown
│   ├── AttractionList.tsx   # Categorized attractions
│   ├── ItineraryView.tsx    # Markdown itinerary renderer
│   └── TipsSection.tsx      # Practical tips and advice
├── lib/
│   ├── api.ts               # API client and types
│   └── utils.ts             # Utility functions
├── styles/
│   └── globals.css          # Global styles and Tailwind
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── next.config.js
```

## API Integration

The frontend communicates with the FastAPI backend at `NEXT_PUBLIC_API_URL`.

### Main Endpoint

**POST /plan**

Request:
```typescript
{
  destination: string;
  origin?: string;
  travel_month?: string;
  budget_level?: 'tight' | 'moderate' | 'flexible';
  interests?: string[];
  trip_type?: 'solo' | 'couple' | 'family' | 'friends';
  duration_days?: number;
}
```

Response:
```typescript
{
  destination: string;
  best_dates: string;
  weather_summary: string;
  flight_options: FlightOption[];
  hotel_options: HotelOption[];
  budget_estimate: BudgetEstimate;
  attractions: Record<string, Attraction[]>;
  itinerary: string;  // Markdown
  tips: any;
  execution_time?: number;
}
```

## Components

### SearchForm

Main form for entering travel preferences.

Props:
- `onSubmit: (data: TravelPlanRequest) => void`
- `isLoading: boolean`

### FlightList

Displays flight options with prices and duration.

Props:
- `flights: FlightOption[]`
- `origin?: string`
- `destination?: string`

### HotelList

Shows hotel options by area and price.

Props:
- `hotels: HotelOption[]`

### BudgetSummary

Displays budget breakdown for three tiers.

Props:
- `budgets: { tight?, moderate?, flexible? }`

### AttractionList

Categorized attractions with ratings.

Props:
- `attractions: Record<string, Attraction[]>`

### ItineraryView

Renders markdown itinerary with styling.

Props:
- `itinerary: string`

### TipsSection

Displays practical travel advice.

Props:
- `tips: any`

## Styling

The app uses Tailwind CSS with custom components:

- `btn-primary` - Primary action buttons
- `btn-secondary` - Secondary buttons
- `card` - Content cards
- `input-field` - Form inputs
- `label` - Form labels

### Dark Mode

Dark mode is automatically supported via Tailwind's dark mode classes.

## Development

### Adding New Components

1. Create component in `components/`
2. Use TypeScript for type safety
3. Import types from `lib/api.ts`
4. Follow existing patterns for styling

### Modifying API Client

Edit `lib/api.ts` to:
- Add new endpoints
- Update request/response types
- Change API URL

### Customizing Styles

Edit `styles/globals.css` for:
- Global styles
- Custom component classes
- Markdown styling

## Deployment

### Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

Set environment variable:
- `NEXT_PUBLIC_API_URL`: Your backend URL

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

Build and run:
```bash
docker build -t travel-planner-frontend .
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://api:8000 travel-planner-frontend
```

### Static Export

For static hosting:

```bash
npm run build
```

This creates an optimized production build in `.next/`.

## Troubleshooting

### CORS Issues

Ensure the backend has CORS enabled for your frontend URL.

Backend should have:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API Connection Errors

1. Check `NEXT_PUBLIC_API_URL` is correct
2. Verify backend is running
3. Check network tab for request details

### Build Errors

Clear cache and reinstall:
```bash
rm -rf .next node_modules package-lock.json
npm install
npm run dev
```

## License

MIT
