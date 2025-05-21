'use client';
import React, { useEffect, useState, CSSProperties } from 'react';
import { Table, Card, Row, Col, Typography, Tooltip, Divider } from 'antd';

const { Title, Text } = Typography;

// CSS keyframes for pulsing animation
const pulseAnimation = `
  @keyframes pulse {
    0% {
      box-shadow: 0 0 0 0 rgba(52, 152, 219, 0.5);
    }
    70% {
      box-shadow: 0 0 0 6px rgba(52, 152, 219, 0);
    }
    100% {
      box-shadow: 0 0 0 0 rgba(52, 152, 219, 0);
    }
  }
`;

// Ultra clean water droplets
const WashIcon = () => (
  <svg 
    width="18" 
    height="18" 
    viewBox="0 0 24 24" 
    style={{ 
      position: 'absolute', 
      top: '2px', 
      left: '2px',
      filter: 'drop-shadow(0px 1px 2px rgba(0,0,0,0.9))',
      zIndex: 5
    }}
  >
    {/* Three classic water droplets */}
    <path d="M6,4 C6,4 4,7 4,8 C4,9.1 5.3,9.1 6,8 C6.7,9.1 8,9.1 8,8 C8,7 6,4 6,4 Z" fill="#ffffff" />
    <path d="M12,7 C12,7 10,10 10,11 C10,12.1 11.3,12.1 12,11 C12.7,12.1 14,12.1 14,11 C14,10 12,7 12,7 Z" fill="#ffffff" />
    <path d="M18,4 C18,4 16,7 16,8 C16,9.1 17.3,9.1 18,8 C18.7,9.1 20,9.1 20,8 C20,7 18,4 18,4 Z" fill="#ffffff" />
  </svg>
);

// Alternative Option 2: Minimalistic Watering Can
const WateringCanIcon = () => (
  <svg 
    width="14" 
    height="14" 
    viewBox="0 0 24 24" 
    fill="#3498db" 
    style={{ 
      position: 'absolute', 
      top: '3px', 
      right: '3px',
      filter: 'drop-shadow(0px 1px 1px rgba(0,0,0,0.3))',
      zIndex: 5
    }}
  >
    <path d="M4,2L6,2L6,4L4,4L4,2Z" />
    <path d="M6,4L8,4L8,6L6,6L6,4Z" />
    <path d="M8,6L10,6L10,8L8,8L8,6Z" />
    <path d="M10,8L12,8L12,10L10,10L10,8Z" />
    <path d="M12,10L14,10L14,12L12,12L12,10Z" />
    <path d="M14,12L16,12L16,14L14,14L14,12Z" />
    <path d="M16,14L18,14L18,16L16,16L16,14Z" />
    <path d="M18,16L20,16L20,18L18,18L18,16Z" />
  </svg>
);

// Alternative Option 3: Minimalistic Sprinkler
const SprinklerIcon = () => (
  <svg 
    width="14" 
    height="14" 
    viewBox="0 0 24 24" 
    fill="#3498db" 
    style={{ 
      position: 'absolute', 
      top: '3px', 
      right: '3px',
      filter: 'drop-shadow(0px 1px 1px rgba(0,0,0,0.3))',
      zIndex: 5
    }}
  >
    <path d="M12,2L12,4L12,6L12,8L12,10L12,12L12,14L12,16L12,18L12,20L12,22" />
    <path d="M2,12L4,12L6,12L8,12L10,12L12,12L14,12L16,12L18,12L20,12L22,12" />
    <path d="M4,4L6,6L8,8L10,10L12,12L14,14L16,16L18,18L20,20" />
    <path d="M20,4L18,6L16,8L14,10L12,12L10,14L8,16L6,18L4,20" />
  </svg>
);

// Simple centered neon green leaf icon
const FertilizerLeafIcon = () => (
  <svg 
    width="18" 
    height="18" 
    viewBox="0 0 18 18" 
    style={{ 
      position: 'absolute', 
      bottom: '2px', 
      right: '2px',
      filter: 'drop-shadow(0px 1px 1px rgba(0,0,0,0.3))',
      zIndex: 5
    }}
  >
    {/* Single neon green leaf - positioned even higher */}
    <g transform="translate(9, 5) scale(0.6)">
      <path 
        d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,8 17,8 17,8Z" 
        fill="#7FD34D"
        transform="translate(-12, 0)"
      />
    </g>
  </svg>
);

// Update the Plant interface to include washing information
interface Plant {
  id: number;
  name: string;
  last_watered: string | null;
  last_fertilized: string | null;
  last_washed: string | null;
  days_since_watering: number | null;
  days_since_fertilizing: number | null;
  days_since_washing: number | null;
  watering_schedule: number;
  fertilizing_schedule: number;
}

// Update the WateringHistoryData interface to include washing dates
interface WateringHistoryData {
  plant_name: string;
  watering_dates: string[]; // Array of dates when the plant was watered
  fertilizing_dates: string[]; // Array of dates when the plant was fertilized
  washing_dates: string[]; // Array of dates when the plant was washed
}

// Update the generateWateringHistory function to include washing events
function generateWateringHistory(
  plantName: string, 
  wateringHistory: WateringHistoryData[], 
  daysAgo: number | null, 
  periodicity: number
): {
  history: boolean[], 
  fertilized: boolean[],
  washed: boolean[],
  today: number, 
  nextWatering: number, 
  isMissedWatering: boolean,
  weekdays: string[]
} {
  const pastDays = 30; // Show last 30 days
  const futureDays = 10; // Show next 10 days
  const totalDays = pastDays + futureDays;
  const history: boolean[] = Array(totalDays).fill(false);
  const fertilized: boolean[] = Array(totalDays).fill(false);
  const washed: boolean[] = Array(totalDays).fill(false);
  const weekdays: string[] = Array(totalDays).fill('');
  
  // Find watering history for this specific plant
  const plantHistory = wateringHistory.find(h => h.plant_name === plantName);
  
  // Debug: Log washing dates for this plant
  console.log(`Washing dates for ${plantName}:`, plantHistory?.washing_dates || []);
  
  // Calculate today's position in the array
  const todayIndex = pastDays - 1;
  
  // Default value for next watering (if we can't calculate it)
  let nextWateringIndex = -1;
  let isMissedWatering = false;
  
  // Get today's date
  const today = new Date();
  const todayStr = `${today.getDate().toString().padStart(2, '0')}.${(today.getMonth() + 1).toString().padStart(2, '0')}.${today.getFullYear()}`;
  
  // Fill in weekdays array
  for (let i = 0; i < totalDays; i++) {
    const date = new Date(today);
    date.setDate(today.getDate() - (pastDays - 1 - i));
    const weekdayLetters = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];
    weekdays[i] = weekdayLetters[date.getDay()];
  }
  
  if (!plantHistory) return { history, fertilized, washed, today: todayIndex, nextWatering: nextWateringIndex, isMissedWatering, weekdays };

  // Convert dates to Date objects
  const wateringDates = plantHistory.watering_dates.map(dateStr => {
    const parts = dateStr.split('.');
    return new Date(parseInt(parts[2]), parseInt(parts[1]) - 1, parseInt(parts[0]));
  });
  
  const fertilizingDates = plantHistory.fertilizing_dates.map(dateStr => {
    const parts = dateStr.split('.');
    return new Date(parseInt(parts[2]), parseInt(parts[1]) - 1, parseInt(parts[0]));
  });

  const washingDates = plantHistory.washing_dates.map(dateStr => {
    const parts = dateStr.split('.');
    return new Date(parseInt(parts[2]), parseInt(parts[1]) - 1, parseInt(parts[0]));
  });
  
  // Sort dates
  wateringDates.sort((a, b) => a.getTime() - b.getTime());
  fertilizingDates.sort((a, b) => a.getTime() - b.getTime());
  washingDates.sort((a, b) => a.getTime() - b.getTime());
  
  // Mark events in the past
  for (let i = 0; i < pastDays; i++) {
    const date = new Date(today);
    date.setDate(today.getDate() - (pastDays - 1 - i));
    
    // Check watering
    const watered = wateringDates.some(waterDate => 
      waterDate.getDate() === date.getDate() && 
      waterDate.getMonth() === date.getMonth() && 
      waterDate.getFullYear() === date.getFullYear()
    );
    
    if (watered) {
      history[i] = true;
      
      // Check if also fertilized on this date
      const fertilizedOnThisDay = fertilizingDates.some(fertilizeDate => 
        fertilizeDate.getDate() === date.getDate() && 
        fertilizeDate.getMonth() === date.getMonth() && 
        fertilizeDate.getFullYear() === date.getFullYear()
      );
      
      if (fertilizedOnThisDay) {
        fertilized[i] = true;
      }

      // Check if also washed on this date
      const washedOnThisDay = washingDates.some(washDate => 
        washDate.getDate() === date.getDate() && 
        washDate.getMonth() === date.getMonth() && 
        washDate.getFullYear() === date.getFullYear()
      );
      
      if (washedOnThisDay) {
        washed[i] = true;
      }
    }
  }
  
  // Calculate next watering date based on periodicity and most recent watering
  if (wateringDates.length > 0 && periodicity > 0) {
    // Get the most recent watering date
    const lastWatering = wateringDates[wateringDates.length - 1];

    // Round fractional cycles (e.g. 4.7 → 5 days) so we work with whole-day offsets
    const roundedPeriodicity = Math.round(periodicity);

    const nextWateringDate = new Date(lastWatering);
    nextWateringDate.setDate(nextWateringDate.getDate() + roundedPeriodicity);

    // Determine the signed distance (in days) between today and that date
    const oneDayMs = 1000 * 60 * 60 * 24;
    const daysUntilNextWatering = Math.floor(
      (nextWateringDate.getTime() - today.getTime()) / oneDayMs
    );

    // Compute the index of that scheduled day within the history/future window
    nextWateringIndex = todayIndex + daysUntilNextWatering;

    // Flag if the watering was missed (scheduled day lies strictly in the past)
    isMissedWatering = daysUntilNextWatering < 0;

    // Only keep the index if it actually falls inside the visualised window
    if (nextWateringIndex < 0 || nextWateringIndex >= history.length) {
      nextWateringIndex = -1; // hidden – outside our 30-past/10-future range
    }
  }
  
  // Debug: Log washed days
  console.log(`Washed days for ${plantName}:`, washed.reduce((acc, isWashed, index) => {
    if (isWashed) acc.push(index);
    return acc;
  }, [] as number[]));
  
  return { history, fertilized, washed, today: todayIndex, nextWatering: nextWateringIndex, isMissedWatering, weekdays };
}

// Update the WateringHistory component to show washing indicators
function WateringHistory({ 
  history, 
  fertilized,
  washed,
  today, 
  nextWatering, 
  isMissedWatering,
  weekdays 
}: { 
  history: boolean[], 
  fertilized: boolean[],
  washed: boolean[],
  today: number, 
  nextWatering: number,
  isMissedWatering: boolean,
  weekdays: string[]
}) {
  // Find watering events and calculate days between them
  const wateringPositions: number[] = [];
  const daysBetween: {startPos: number, endPos: number, days: number}[] = [];
  
  // Find all watering positions in the history
  history.forEach((watered, i) => {
    if (watered) wateringPositions.push(i);
  });
  
  // Calculate days between consecutive waterings
  for (let i = 0; i < wateringPositions.length - 1; i++) {
    const start = wateringPositions[i];
    const end = wateringPositions[i + 1];
    const days = end - start;
    daysBetween.push({startPos: start, endPos: end, days});
  }
  
  return (
    <div>
      {/* Main timeline */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '3px', height: '50px', width: '100%', position: 'relative' }}>
        {history.map((watered, i) => {
          // Determine if this is past, today, or future
          const isPast = i < today;
          const isToday = i === today;
          const isFuture = i > today;
          const isNextWatering = i === nextWatering;
          
          // Determine all possible combinations
          const isTodayAndNextWatering = isToday && isNextWatering && !watered; // Only show next watering if not already watered
          const isTodayAndWatered = isToday && watered;
          
          // Set base style
          let style: CSSProperties = {
            width: '100%',
            height: '50px',
            backgroundColor: 'var(--color-not-watered)',
            borderRadius: isPast ? '6px' : '8px',
            flexGrow: 1,
            flexBasis: 0,
            border: 'none',
            position: 'relative'
          };
          
          // Apply appropriate style based on combinations
          
          // Case 1: Today + Next Watering (only if not already watered)
          if (isTodayAndNextWatering) {
            style = {
              ...style,
              // Keep a clean background with just the green dashed border
              backgroundColor: 'var(--color-not-watered)',
              border: isMissedWatering ? 
                '2px dashed #F0C040' : // Yellow for missed watering
                '2px dashed var(--color-watered)', // Green for due today
              // Keep the pulsing animation
              animation: 'pulse 2s infinite'
            };
          }
          // Case 2: Today + Past Watering (user watered today)
          else if (isTodayAndWatered) {
            style = {
              ...style,
              backgroundColor: 'var(--color-watered)',
              // Add the today border to show it's today
              border: '2px solid var(--color-today-border)'
            };
          }
          // Case 3: Just Today
          else if (isToday) {
            style = {
              ...style,
              border: '2px solid var(--color-today-border)',
              backgroundColor: 'var(--color-not-watered)'
            };
          }
          // Case 4: Just Next Watering
          else if (isNextWatering) {
            style = {
              ...style,
              border: isMissedWatering ? 
                '2px dashed #F0C040' : // Yellow for missed watering
                '2px dashed var(--color-watered)', // Green for future watering
              backgroundColor: 'var(--color-not-watered)'
            };
            
            // Add diagonal pattern for forecast period (future days)
            if (isFuture) {
              style = {
                ...style,
                backgroundImage: 'linear-gradient(45deg, var(--color-not-watered) 25%, #E0E0E0 25%, #E0E0E0 50%, var(--color-not-watered) 50%, var(--color-not-watered) 75%, #E0E0E0 75%, #E0E0E0 100%)',
                backgroundSize: '10px 10px'
              };
            }
          }
          // Case 5: Just Past Watering
          else if (watered) {
            style = {
              ...style,
              backgroundColor: 'var(--color-watered)',
              border: 'none'
            };
          }
          
          // Style adjustments for future items (forecast) - only apply to regular future days, not next watering
          if (isFuture && !isNextWatering) {
            style = {
              ...style,
              backgroundColor: style.backgroundColor === 'var(--color-watered)' ? 'var(--color-watered-light)' : style.backgroundColor,
              backgroundImage: style.backgroundColor === 'var(--color-not-watered)' ? 
                'linear-gradient(45deg, var(--color-not-watered) 25%, #E0E0E0 25%, #E0E0E0 50%, var(--color-not-watered) 50%, var(--color-not-watered) 75%, #E0E0E0 75%, #E0E0E0 100%)' : 
                'none',
              backgroundSize: '10px 10px'
            };
          }
          
          // Calculate the date for this position
          const totalDays = history.length;
          const pastDays = today + 1;
          const daysFromToday = i - today;
          
          // Get date for this position to add to tooltip
          let date = new Date();
          date.setDate(date.getDate() + daysFromToday);
          const weekdayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
          const weekday = weekdayNames[date.getDay()];
          
          // Create tooltip text that shows all applicable states
          let tooltipText = '';
          
          // Today + Next Watering
          if (isTodayAndNextWatering) {
            tooltipText = isMissedWatering ? 
              `Today (${weekday}): Missed watering!` :
              `Today (${weekday}): Next watering due`;
          }
          // Today + Past Watering
          else if (isTodayAndWatered) {
            tooltipText = `Today (${weekday}): Already watered`;
          }
          // Past days
          else if (i < today) {
            if (isNextWatering && isMissedWatering) {
              tooltipText = `${weekday}, ${Math.abs(daysFromToday)} days ago: Missed watering!`;
            } else {
              tooltipText = `${weekday}, ${Math.abs(daysFromToday)} days ago: ${watered ? 'Watered' : 'Not watered'}`;
            }
          }
          // Just Today
          else if (isToday) {
            tooltipText = `Today (${weekday})`;
          }
          // Just Next Watering
          else if (isNextWatering) {
            tooltipText = `${weekday}, ${daysFromToday} days from now: Next watering`;
          }
          // Future days
          else {
            tooltipText = `${weekday}, ${daysFromToday} days from now`;
          }
          
          return (
            <Tooltip key={i} title={tooltipText}>
              <div style={style}>
                {/* Add shower icon for washing events */}
                {washed[i] && <WashIcon />}
                
                {/* Add fertilizer leaf icon if fertilized on this day */}
                {watered && fertilized[i] && <FertilizerLeafIcon />}
              </div>
            </Tooltip>
          );
        })}
        
        {/* Day count badges */}
        {daysBetween.map((interval, index) => {
          const startPos = interval.startPos;
          const endPos = interval.endPos;
          const midpoint = startPos + (endPos - startPos) / 2;
          
          // Skip future intervals (we only want to show past watering intervals)
          if (startPos >= today) return null;
          
          // Calculate position as percentage of total width
          const leftPosition = (midpoint / history.length) * 100;
          
          return (
            <div 
              key={`interval-${index}`}
              style={{
                position: 'absolute',
                left: `${leftPosition}%`,
                top: '-10px',
                transform: 'translateX(-50%)',
                backgroundColor: 'rgba(255, 255, 255, 0.6)',
                border: '1px solid rgba(125, 157, 133, 0.3)',
                borderRadius: '8px',
                padding: '0px 3px',
                fontSize: '9px',
                fontWeight: '500',
                color: 'var(--color-text-secondary)',
                zIndex: 10,
                boxShadow: '0 1px 1px rgba(0,0,0,0.05)'
              }}
            >
              {interval.days}d
            </div>
          );
        })}
      </div>
      
      {/* Weekday indicators below - one for each day */}
      <div style={{ display: 'flex', alignItems: 'center', marginTop: '2px', gap: '3px', height: '16px' }}>
        {weekdays.map((day, i) => {
          // Determine if it's a weekend (S) or today
          const isWeekend = day === 'S';
          const isToday = i === today;
          
          return (
            <div 
              key={i}
              style={{ 
                flexGrow: 1,
                flexBasis: 0,
                textAlign: 'center',
                fontSize: '9px',
                fontFamily: "'Quicksand', sans-serif",
                fontWeight: isWeekend ? '600' : '500',
                color: isWeekend ? 'var(--color-text-primary)' : 'var(--color-text-secondary)', // Darker color for weekends
                backgroundColor: isToday ? 'rgba(125, 157, 133, 0.15)' : 'transparent', // Subtle green highlight for today
                borderRadius: '3px',
                padding: '2px 0'
              }}
            >
              {day}
            </div>
          );
        })}
      </div>
    </div>
  );
}

// Explicit mapping from normalized plant names to image filenames
const imageMap: Record<string, string> = {
  'epipremnum_aureum': 'epipremnum_aureum.jpg',
  'coffea_arabica': 'coffea_arabica.jpg',
  'philodendron_hedaracium_brasil': 'philodendron_brasil.jpeg',
  'philodendron_scandens_micans': 'philodendron_micans.jpg',
  'scindapsus_treubii_moonlight': 'scindapsus_treubii_moonlight.jpg',
  'calathea_medalion': 'calathea_medallion.jpeg',
  'calathea_orbifolia': 'calathea_orbifolia.png',
  'monstera_adenossii': 'monstera_adansonii.jpg',
  'ficus_elastica_abidjan': 'ficus_abidjan.jpg',
  'calathea_ornata': 'calathea_ornata.jpg',
  'beaucarnea_recurvata': 'beaucarnea_recurvata.jpg',
  'nephrolepis_obliterata': 'nephrolepis_obliterata.jpg',
  'peperomia_hope': 'peperomia_hope.jpg',
  'hoya_mathilde': 'hoya_mathilde.jpg'};

function getImageSrc(plantName: string) {
  const base = plantName
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9 ]/g, '')
    .replace(/\s+/g, '_');
  if (imageMap[base]) {
    return `/plant_images/${imageMap[base]}`;
  }
  return '/plant_images/default.jpg';
}

// Helper function to format days ago text
function formatDaysAgo(days: number | null): string {
  if (days === null) return 'never';
  if (days === 0) return 'today';
  if (days === 1) return 'yesterday';
  return `${days} days ago`;
}

export default function PlantOverview() {
  const [plants, setPlants] = useState<Plant[]>([]);
  const [loading, setLoading] = useState(true);
  const [periodicities, setPeriodicities] = useState<Record<string, number>>({});
  const [wateringHistory, setWateringHistory] = useState<WateringHistoryData[]>([]);

  useEffect(() => {
    // Fetch plants data - using relative URLs instead of hardcoded localhost
    fetch('/api/plants/today')
      .then(res => res.json())
      .then(data => {
        // If watering_schedule and fertilizing_schedule are missing, add defaults
        const enhancedData = data.map((plant: any) => ({
          ...plant,
          watering_schedule: plant.watering_schedule || 7,
          fertilizing_schedule: plant.fertilizing_schedule || 14
        }));
        setPlants(enhancedData);
        setLoading(false);
      });
    
    // Fetch watering periodicity data - using relative URLs
    fetch('/api/plants/periodicity')
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          // Create a mapping of plant name to calculated periodicity
          const periodicityMap: Record<string, number> = {};
          data.data.forEach((item: any) => {
            if (item.calculated_periodicity !== null) {
              periodicityMap[item.plant_name] = item.calculated_periodicity;
            }
          });
          setPeriodicities(periodicityMap);
        }
      })
      .catch(error => {
        console.error("Error fetching periodicity data:", error);
      });

    // Fetch raw plant data to extract both watering and fertilizing history
    fetch('/api/plants')
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          // Process the data to extract watering and fertilizing dates for each plant
          const plantWateringMap: Record<string, {watering: string[], fertilizing: string[], washing: string[]}> = {};
          
          // Debug: Log all entries with wash data
          console.log("All entries with wash column:", data.data.filter((entry: any) => 
            entry.wash !== undefined && entry.wash !== null && entry.wash !== ''
          ));
          
          data.data.forEach((entry: any) => {
            const plantName = entry['plant name'];
            const date = entry.date;
            const daysWithoutWater = entry['days without water'];
            const waterEntry = entry.water;
            const fertilizerEntry = entry.fertilizer;
            const washEntry = entry.wash;
            
            // Debug: Log wash entries
            if (washEntry !== undefined && washEntry !== null && washEntry !== '') {
              console.log(`Found wash entry for ${plantName} on ${date}: ${washEntry}`);
            }
            
            if (plantName && date) {
              if (!plantWateringMap[plantName]) {
                plantWateringMap[plantName] = {watering: [], fertilizing: [], washing: []};
              }
              
              // Check if this row indicates a watering event
              const isWateringEvent = 
                daysWithoutWater === 0 || 
                (typeof daysWithoutWater === 'string' && daysWithoutWater.trim() === '0') || 
                waterEntry;
                
              if (isWateringEvent) {
                plantWateringMap[plantName].watering.push(date);
              }
              
              // Check if this row indicates a fertilizing event
              if (fertilizerEntry) {
                plantWateringMap[plantName].fertilizing.push(date);
              }

              // Check if this row indicates a washing event
              if (washEntry !== undefined && washEntry !== null && washEntry !== '') {
                plantWateringMap[plantName].washing.push(date);
              }
            }
          });
          
          // Debug: Log wash events for each plant  
          console.log("All wash events:", Object.entries(plantWateringMap).map(([plant, data]) => ({
            plant,
            washing_dates: data.washing
          })).filter(item => item.washing_dates.length > 0));
          
          // Convert to array format for state
          const wateringHistoryData = Object.entries(plantWateringMap).map(([plant_name, data]) => ({
            plant_name,
            watering_dates: data.watering,
            fertilizing_dates: data.fertilizing,
            washing_dates: data.washing
          }));
          
          setWateringHistory(wateringHistoryData);
        }
      })
      .catch(error => {
        console.error("Error fetching plant data for history:", error);
      });
  }, []);

  // Custom render function for each plant card
  const renderPlantCard = (plant: Plant) => {
    // Get the calculated periodicity or fall back to the default watering schedule
    const periodicity = periodicities[plant.name] || plant.watering_schedule;
    
    // Get watering history with today and next watering indicators
    const { history, fertilized, washed, today, nextWatering, isMissedWatering, weekdays } = generateWateringHistory(
      plant.name, 
      wateringHistory, 
      plant.days_since_watering,
      periodicity
    );
    
    return (
      <Card 
        key={plant.id} 
        style={{ marginBottom: 24 }}
        bodyStyle={{ padding: 24 }}
      >
        {/* Top section - Plant Info */}
        <Row gutter={[16, 16]} align="top">
          {/* Left column - Plant Image */}
          <Col xs={24} sm={6} md={4} style={{ textAlign: 'center' }}>
            <img
              src={getImageSrc(plant.name)}
              alt={plant.name}
              style={{ 
                width: '100%', 
                maxWidth: 140, 
                height: 140, 
                objectFit: 'cover', 
                borderRadius: 12,
                marginBottom: 8,
                boxShadow: '0 4px 8px rgba(59, 46, 30, 0.1)'
              }}
            />
          </Col>
          
          {/* Right column - Plant Info */}
          <Col xs={24} sm={18} md={20}>
            <div style={{ marginBottom: 16 }}>
              <Title level={4} style={{ marginBottom: 12, fontFamily: "'Quicksand', sans-serif", fontWeight: 600 }}>{plant.name}</Title>
              <Row gutter={24}>
                <Col xs={24} sm={12}>
                  <Text strong>Last Watered:</Text><br />
                  <Text>{plant.last_watered ? `${plant.last_watered} (${formatDaysAgo(plant.days_since_watering)})` : 'Never'}</Text>
                </Col>
                <Col xs={24} sm={12}>
                  <Text strong>Last Fertilized:</Text><br />
                  <Text>{plant.last_fertilized ? `${plant.last_fertilized} (${formatDaysAgo(plant.days_since_fertilizing)})` : 'Never'}</Text>
                </Col>
              </Row>
            </div>
          </Col>
        </Row>
        
        <Divider style={{ margin: '16px 0' }} />
        
        {/* Bottom section - Full Width Watering History */}
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 14 }}>
            <Text strong style={{ fontSize: 16, fontFamily: "'Quicksand', sans-serif", color: 'var(--color-text-primary)' }}>Watering History & Forecast</Text>
            <Text type="secondary" style={{ fontFamily: "'Quicksand', sans-serif" }}>Watering Cycle: {periodicity} days</Text>
          </div>
          
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <div style={{ flex: 1 }}>
              <WateringHistory 
                history={history}
                fertilized={fertilized}
                washed={washed}
                today={today} 
                nextWatering={nextWatering}
                isMissedWatering={isMissedWatering}
                weekdays={weekdays}
              />
            </div>
          </div>
          
          {/* Legend */}
          <div style={{ marginTop: 14, display: 'flex', gap: 16, justifyContent: 'flex-end' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
              <div style={{ width: 16, height: 16, position: 'relative', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <svg viewBox="0 0 18 18" width="16" height="16" style={{ display: 'block' }}>
                  <g transform="translate(9, 5) scale(0.6)">
                    <path 
                      d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,8 17,8 17,8Z" 
                      fill="#7FD34D"
                      transform="translate(-12, 0)"
                    />
                  </g>
                </svg>
              </div>
              <Text type="secondary" style={{ fontSize: 12, lineHeight: 1 }}>Fertilized</Text>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
              <div style={{ width: 16, height: 16, backgroundColor: 'var(--color-watered)', borderRadius: 4 }}></div>
              <Text type="secondary" style={{ fontSize: 12 }}>Past Watering</Text>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
              <div style={{ width: 16, height: 16, border: '2px solid var(--color-today-border)', borderRadius: 4 }}></div>
              <Text type="secondary" style={{ fontSize: 12 }}>Today</Text>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
              <div style={{ width: 16, height: 16, border: '2px dashed var(--color-watered)', borderRadius: 6, backgroundImage: 'linear-gradient(45deg, var(--color-not-watered) 25%, #E0E0E0 25%, #E0E0E0 50%, var(--color-not-watered) 50%, var(--color-not-watered) 75%, #E0E0E0 75%, #E0E0E0 100%)', backgroundSize: '10px 10px' }}></div>
              <Text type="secondary" style={{ fontSize: 12 }}>Next Watering</Text>
            </div>
          </div>
        </div>
      </Card>
    );
  };

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '20px 16px' }}>
      {/* Add style element for animation */}
      <style>{pulseAnimation}</style>
      
      <Title level={2} style={{ marginBottom: 24, fontFamily: "'Quicksand', sans-serif", fontWeight: 700, color: 'var(--color-text-primary)' }}>Plants Overview</Title>
      
      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px 0' }}>
          <Text>Loading plants...</Text>
        </div>
      ) : (
        <div>
          {plants.map(renderPlantCard)}
        </div>
      )}
    </div>
  );
} 