'use client';
import React, { useEffect, useState, CSSProperties, useMemo } from 'react';
import { Table, Card, Row, Col, Typography, Tooltip, Divider, Button, Tag } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined, FilterOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

// CSS keyframes for pulsing animation
const pulseAnimation = `
  @keyframes pulse {
    0% {
      box-shadow: 0 0 0 0 rgba(52, 152, 219, 0.7); /* Increased opacity */
    }
    70% {
      box-shadow: 0 0 0 10px rgba(52, 152, 219, 0); /* Increased spread */
    }
    100% {
      box-shadow: 0 0 0 0 rgba(52, 152, 219, 0);
    }
  }
`;

// Water droplet SVG icon for "water today" indicator
const WaterDropletIcon = () => (
  <svg 
    width="100%" 
    height="100%" 
    viewBox="0 0 24 24" 
    fill="#3498db" 
    style={{ 
      position: 'absolute', 
      top: '10%', 
      right: '10%',
      width: '60%',           // scale with strip width
      height: 'auto',
      zIndex: 5,
      pointerEvents: 'none'
    }}
  >
    <path d="M12,20A6,6 0 0,1 6,14C6,10 12,3.25 12,3.25C12,3.25 18,10 18,14A6,6 0 0,1 12,20Z" />
  </svg>
);

// Simple centered neon green leaf icon
const FertilizerLeafIcon = () => (
  <svg 
    width="100%" 
    height="100%" 
    viewBox="0 0 18 18" 
    style={{ 
      position: 'absolute', 
      bottom: '10%', 
      right: '10%',
      width: '70%',          // scale with strip width
      height: 'auto',
      zIndex: 5,
      pointerEvents: 'none'
    }}
  >
    {/* Single neon green leaf */}
    <g transform="translate(9, 5) scale(0.6)">
      <path 
        d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 2,11.5 2,13.5C2,15.5 3.75,17.25 3.75,17.25C7,8 17,8 17,8Z" 
        fill="#7FD34D"
        transform="translate(-12, 0)"
      />
    </g>
  </svg>
);

// Water spray icon for washing plants
const WashingSprayIcon = ({ fillColor }: { fillColor?: string }) => (
  <svg 
    width="100%" 
    height="100%" 
    viewBox="0 0 24 24" 
    style={{ 
      position: 'absolute',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      width: '80%',          // scale with strip
      height: 'auto',
      zIndex: 6,
      pointerEvents: 'none'
    }}
  >
    {/* Three water droplets - universal washing symbol */}
    <g>
      {/* Center/main droplet */}
      <path 
        d="M12,3.77L11.25,4.61C11.25,4.61 9.97,6.06 8.68,7.94C7.39,9.82 6,12.07 6,14.23A6,6 0 0,0 12,20.23A6,6 0 0,0 18,14.23C18,12.07 16.61,9.82 15.32,7.94C14.03,6.06 12.75,4.61 12.75,4.61L12,3.77M12,6.9C12.44,7.42 12.84,7.85 13.68,9.07C14.89,10.83 16,13.07 16,14.23C16,16.45 14.22,18.23 12,18.23C9.78,18.23 8,16.45 8,14.23C8,13.07 9.11,10.83 10.32,9.07C11.16,7.85 11.56,7.42 12,6.9Z" 
        fill={fillColor || '#FAFAFA'} // Default to very light grey if no prop passed
      />
      {/* Left droplet */}
      <path 
        d="M7,2.77L6.25,3.61C6.25,3.61 4.97,5.06 3.68,6.94C2.39,8.82 1,11.07 1,13.23A6,6 0 0,0 7,19.23A6,6 0 0,0 13,13.23C13,11.07 11.61,8.82 10.32,6.94C9.03,5.06 7.75,3.61 7.75,3.61L7,2.77M7,5.9C7.44,6.42 7.84,6.85 8.68,8.07C9.89,9.83 11,12.07 11,13.23C11,15.45 9.22,17.23 7,17.23C4.78,17.23 3,15.45 3,13.23C3,12.07 4.11,9.83 5.32,8.07C6.16,6.85 6.56,6.42 7,5.9Z" 
        fill={fillColor || '#FAFAFA'} // Default to very light grey
        transform="scale(0.7) translate(0, 2)"
      />
      {/* Right droplet */}
      <path 
        d="M17,2.77L16.25,3.61C16.25,3.61 14.97,5.06 13.68,6.94C12.39,8.82 11,11.07 11,13.23A6,6 0 0,0 17,19.23A6,6 0 0,0 23,13.23C23,11.07 21.61,8.82 20.32,6.94C19.03,5.06 17.75,3.61 17.75,3.61L17,2.77M17,5.9C17.44,6.42 17.84,6.85 18.68,8.07C19.89,9.83 21,12.07 21,13.23C21,15.45 19.22,17.23 17,17.23C14.78,17.23 13,15.45 13,13.23C13,12.07 14.11,9.83 15.32,8.07C16.16,6.85 16.56,6.42 17,5.9Z" 
        fill={fillColor || '#FAFAFA'} // Default to very light grey
        transform="scale(0.7) translate(8, 2)"
      />
    </g>
  </svg>
);

interface Plant {
  id: number;
  name: string;
  last_watered: string | null;
  last_fertilized: string | null;
  days_since_watering: number | null;
  days_since_fertilizing: number | null;
  watering_schedule: number;
  fertilizing_schedule: number;
}

// Update the interfaces to include washing history
interface WateringHistoryData {
  plant_name: string;
  watering_dates: string[]; // Array of dates when the plant was watered
  fertilizing_dates: string[]; // Array of dates when the plant was fertilized
  washing_dates: string[]; // Array of dates when the plant was washed
  neemoil_dates: string[]; // Array of dates when the plant was treated with neem oil
  pestmix_dates: string[]; // Array of dates when the plant was treated with pest mix
}

// Update the return type of generateWateringHistory
interface WateringHistoryResult {
  history: boolean[], 
  fertilized: boolean[], 
  washed: boolean[],
  neemoiled: boolean[], // Existing neem oil treatment
  pestmixed: boolean[], // Added for pest mix treatment
  today: number, 
  nextWatering: number, // This is an index
  isMissedWatering: boolean,
  weekdays: string[],
  actualDaysUntilNextWatering: number | null; // Added for sorting
}

// Update the generateWateringHistory function to track washing events
function generateWateringHistory(
  plantName: string, 
  wateringHistory: WateringHistoryData[], 
  daysAgo: number | null, 
  periodicity: number
): WateringHistoryResult { // Update return type here
  const pastDays = 30; // Show last 30 days
  const futureDays = 10; // Show next 10 days
  const totalDays = pastDays + futureDays;
  const history: boolean[] = Array(totalDays).fill(false);
  const fertilized: boolean[] = Array(totalDays).fill(false); // Track fertilizing events
  const washed: boolean[] = Array(totalDays).fill(false); // Track washing events
  const neemoiled: boolean[] = Array(totalDays).fill(false); // Track neem oil events
  const pestmixed: boolean[] = Array(totalDays).fill(false); // Track pest mix events
  const weekdays: string[] = Array(totalDays).fill('');
  
  // Find watering history for this specific plant
  const plantHistory = wateringHistory.find(h => h.plant_name === plantName);
  
  // Calculate today's position in the array
  const todayIndex = pastDays - 1;
  
  // Default value for next watering (if we can't calculate it)
  let nextWateringIndex = -1;
  let isMissedWatering = false;
  let actualDaysUntilNextWatering: number | null = null; // Initialize
  
  // Get today's date
  const today = new Date();
  const todayStr = `${today.getDate().toString().padStart(2, '0')}.${(today.getMonth() + 1).toString().padStart(2, '0')}.${today.getFullYear()}`;
  
  // Fill in weekdays array
  for (let i = 0; i < totalDays; i++) {
    const date = new Date(today);
    date.setDate(today.getDate() - (pastDays - 1 - i)); // date for this position
    
    // Get single-letter weekday (M, T, W, T, F, S, S)
    const weekdayLetters = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];
    weekdays[i] = weekdayLetters[date.getDay()];
  }
  
  if (!plantHistory) return { history, fertilized, washed, neemoiled, pestmixed, today: todayIndex, nextWatering: nextWateringIndex, isMissedWatering, weekdays, actualDaysUntilNextWatering };

  // Special handling for days_since_watering = 0 (watered today)
  // If the plant was watered today (according to the API), mark today as watered
  if (daysAgo === 0) {
    history[todayIndex] = true;
  }

  // Convert watering dates to Date objects
  const wateringDates = plantHistory.watering_dates.map(dateStr => {
    const parts = dateStr.split('.');
    return new Date(parseInt(parts[2]), parseInt(parts[1]) - 1, parseInt(parts[0]));
  });
  
  // Convert fertilizing dates to Date objects (if available)
  const fertilizingDates = plantHistory.fertilizing_dates ? plantHistory.fertilizing_dates.map(dateStr => {
    const parts = dateStr.split('.');
    return new Date(parseInt(parts[2]), parseInt(parts[1]) - 1, parseInt(parts[0]));
  }) : [];
  
  // Convert washing dates to Date objects (if available)
  const washingDates = plantHistory.washing_dates ? plantHistory.washing_dates.map(dateStr => {
    const parts = dateStr.split('.');
    return new Date(parseInt(parts[2]), parseInt(parts[1]) - 1, parseInt(parts[0]));
  }) : [];
  
  // Convert neem oil dates to Date objects (if available)
  const neemoilDates = plantHistory.neemoil_dates ? plantHistory.neemoil_dates.map(dateStr => {
    const parts = dateStr.split('.');
    return new Date(parseInt(parts[2]), parseInt(parts[1]) - 1, parseInt(parts[0]));
  }) : [];
  
  // Convert pest mix dates to Date objects (if available)
  const pestmixDates = plantHistory.pestmix_dates ? plantHistory.pestmix_dates.map(dateStr => {
    const parts = dateStr.split('.');
    return new Date(parseInt(parts[2]), parseInt(parts[1]) - 1, parseInt(parts[0]));
  }) : [];
  
  // Sort dates in ascending order
  wateringDates.sort((a, b) => a.getTime() - b.getTime());
  fertilizingDates.sort((a, b) => a.getTime() - b.getTime());
  washingDates.sort((a, b) => a.getTime() - b.getTime());
  neemoilDates.sort((a, b) => a.getTime() - b.getTime());
  pestmixDates.sort((a, b) => a.getTime() - b.getTime());
  
  // Check if today's date is in the watering dates list
  const wateredToday = plantHistory.watering_dates.includes(todayStr);
  if (wateredToday) {
    history[todayIndex] = true;
  }
  
  // Mark watering days in the past
  for (let i = 0; i < pastDays; i++) {
    const date = new Date(today);
    date.setDate(today.getDate() - (pastDays - 1 - i)); // date for this position in history
    
    // Check if this date matches any watering date
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
    }
    
    // Check if washed on this date (independent of watering)
    const washedOnThisDay = washingDates.some(washDate => 
      washDate.getDate() === date.getDate() && 
      washDate.getMonth() === date.getMonth() && 
      washDate.getFullYear() === date.getFullYear()
    );
    
    if (washedOnThisDay) {
      washed[i] = true;
    }
    
    // Check if treated with neem oil on this date (independent of watering/washing)
    const neemoiledOnThisDay = neemoilDates.some(neemoilDate =>
      neemoilDate.getDate() === date.getDate() &&
      neemoilDate.getMonth() === date.getMonth() &&
      neemoilDate.getFullYear() === date.getFullYear()
    );

    if (neemoiledOnThisDay) {
      neemoiled[i] = true;
    }

    // Check if treated with pest mix on this date (independent)
    const pestmixedOnThisDay = pestmixDates.some(pestmixDate =>
      pestmixDate.getDate() === date.getDate() &&
      pestmixDate.getMonth() === date.getMonth() &&
      pestmixDate.getFullYear() === date.getFullYear()
    );

    if (pestmixedOnThisDay) {
      pestmixed[i] = true;
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
    const daysUntilNextWateringCalc = Math.floor( // Renamed to avoid conflict if 'daysUntilNextWatering' is used elsewhere for a different purpose
      (nextWateringDate.getTime() - today.getTime()) / oneDayMs
    );
    actualDaysUntilNextWatering = daysUntilNextWateringCalc; // Store the raw value

    // Compute the index of that scheduled day within the history/future window
    nextWateringIndex = todayIndex + daysUntilNextWateringCalc;

    // Flag if the watering was missed (scheduled day lies strictly in the past)
    isMissedWatering = daysUntilNextWateringCalc < 0;

    // Only keep the index if it actually falls inside the visualised window
    if (nextWateringIndex < 0 || nextWateringIndex >= history.length) {
      nextWateringIndex = -1; // hidden – outside our 30-past/10-future range
    }
  }
  
  // Debug: Check if we have any washing dates
  if (washingDates.length > 0) {
    console.log(`Plant ${plantName} has ${washingDates.length} washing dates`);
    console.log(`Washing dates for ${plantName}:`, washingDates);
    // Check which days are marked as washed in the visualization
    const washedDays = washed.reduce((acc, isWashed, index) => {
      if (isWashed) acc.push(index);
      return acc;
    }, [] as number[]);
    console.log(`Washed days in visualization for ${plantName}:`, washedDays);
  }
  
  return { history, fertilized, washed, neemoiled, pestmixed, today: todayIndex, nextWatering: nextWateringIndex, isMissedWatering, weekdays, actualDaysUntilNextWatering };
}

// Update the WateringHistory component to show washing indicators
function WateringHistory({ 
  history, 
  fertilized, 
  washed,
  neemoiled, // Existing neemoiled
  pestmixed, // Added pestmixed
  today, 
  nextWatering, 
  isMissedWatering,
  weekdays 
}: { 
  history: boolean[], 
  fertilized: boolean[],
  washed: boolean[],
  neemoiled: boolean[], // Existing neemoiled
  pestmixed: boolean[], // Added pestmixed
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
            position: 'relative',
            overflow: 'hidden'          // clip icon shadows and keep them inside
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
              animation: 'pulse 1.5s infinite'
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
                {/* Add water droplet icon ONLY for "needs watering today" case - REMOVED as per user request */}
                {/* {isTodayAndNextWatering && !isMissedWatering && <WaterDropletIcon />} */}
                
                {/* Add fertilizer leaf icon if fertilized on this day */}
                {watered && fertilized[i] && <FertilizerLeafIcon />}
                
                {/* Add washing spray icon if the plant was washed on this day */}
                {washed[i] && !neemoiled[i] && <WashingSprayIcon fillColor={watered ? '#FAFAFA' : '#3498db'} />}

                {/* Show brown WashingSprayIcon if the plant was treated with neem oil on this day */}
                {neemoiled[i] && <WashingSprayIcon fillColor={watered ? '#A0522D' : '#8B4513'} />} {/* Neem Oil */}

                {/* Show purple WashingSprayIcon if the plant was treated with pest mix on this day */}
                {pestmixed[i] && <WashingSprayIcon fillColor={watered ? '#6A0DAD' : '#800080'} />} {/* Pest Mix */}
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
  'philodendron_hedaracium_brasil': 'philodendron_brasil.jpg',
  'philodendron_scandens_micans': 'philodendron_micans.jpg',
  'scindapsus_treubii_moonlight': 'scindapsus_treubii_moonlight.jpg',
  'calathea_medalion': 'calathea_medallion.jpg',
  'calathea_orbifolia': 'calathea_orbifolia.jpg',
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
  
  console.log('Original plant name:', plantName);
  console.log('Transformed base:', base);
  console.log('Image map has this key?', imageMap.hasOwnProperty(base));
  
  if (imageMap[base]) {
    const path = `/plant_images/${imageMap[base]}`;
    console.log('Returning image path:', path);
    return path;
  }
  console.log('Falling back to default.jpg');
  return '/plant_images/default.jpg';
}

// Helper function to format days ago text
function formatDaysAgo(days: number | null): string {
  if (days === null) return 'never';
  if (days === 0) return 'today';
  if (days === 1) return 'yesterday';
  return `${days} days ago`;
}

// Define sort states
type WateringSortState = 'default' | 'urgent' | 'leastUrgent';

// Define a type for plants with sorting keys
interface PlantWithSortKey extends Plant {
  isMissedWatering: boolean;
  actualDaysUntilNextWatering: number | null;
}

export default function PlantOverview() {
  const [plants, setPlants] = useState<Plant[]>([]);
  const [loading, setLoading] = useState(true);
  const [periodicities, setPeriodicities] = useState<Record<string, number>>({});
  const [calculationMethods, setCalculationMethods] = useState<Record<string, string>>({});
  const [wateringHistory, setWateringHistory] = useState<WateringHistoryData[]>([]);
  const [wateringSortState, setWateringSortState] = useState<WateringSortState>('urgent');

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
          const methodMap: Record<string, string> = {};
          data.data.forEach((item: any) => {
            if (item.calculated_periodicity !== null) {
              periodicityMap[item.plant_name] = item.calculated_periodicity;
              methodMap[item.plant_name] = item.calculation_method;
            }
          });
          setPeriodicities(periodicityMap);
          setCalculationMethods(methodMap);
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
          const plantWateringMap: Record<string, {watering: string[], fertilizing: string[], washing: string[], neemoil: string[], pestmix: string[]}> = {};
          
          data.data.forEach((entry: any) => {
            const plantName = entry['plant name'];
            const date = entry.date;
            const daysWithoutWater = entry['days without water'];
            const waterEntry = entry.water;
            const fertilizerEntry = entry.fertilizer;
            const washEntry = entry.wash;
            const neemoilEntry = entry.neemoil; // Existing neem oil
            const pestmixEntry = entry.pestmix; // Added pest mix
            
            if (plantName && date) {
              if (!plantWateringMap[plantName]) {
                plantWateringMap[plantName] = {watering: [], fertilizing: [], washing: [], neemoil: [], pestmix: []}; // Added pestmix
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
              if (washEntry) {
                plantWateringMap[plantName].washing.push(date);
              }
              
              // Check if this row indicates a neem oil event
              if (neemoilEntry) {
                plantWateringMap[plantName].neemoil.push(date);
              }

              // Check if this row indicates a pest mix event
              if (pestmixEntry) {
                plantWateringMap[plantName].pestmix.push(date);
              }
            }
          });
          
          // Convert to array format for state
          const wateringHistoryData = Object.entries(plantWateringMap).map(([plant_name, data]) => ({
            plant_name,
            watering_dates: data.watering,
            fertilizing_dates: data.fertilizing,
            washing_dates: data.washing,
            neemoil_dates: data.neemoil,
            pestmix_dates: data.pestmix
          }));
          
          // Debug: Check if we have any washing dates in our data
          const hasWashing = wateringHistoryData.some(plant => plant.washing_dates && plant.washing_dates.length > 0);
          console.log('Plants with washing history:', hasWashing);
          if (hasWashing) {
            const plantsWithWashing = wateringHistoryData
              .filter(plant => plant.washing_dates && plant.washing_dates.length > 0)
              .map(plant => ({ name: plant.plant_name, washDates: plant.washing_dates }));
            console.log('Washing data:', plantsWithWashing);
          }
          
          setWateringHistory(wateringHistoryData);
        }
      })
      .catch(error => {
        console.error("Error fetching plant data for history:", error);
      });
  }, []);

  // Memoized and sorted list of plants
  const displayedPlants = useMemo(() => {
    // Create a new array with an additional sorting key for each plant
    const plantsWithSortKey: PlantWithSortKey[] = plants.map(plant => {
      const periodicity = periodicities[plant.name] || plant.watering_schedule;
      const { isMissedWatering, actualDaysUntilNextWatering } = generateWateringHistory(
        plant.name,
        wateringHistory,
        plant.days_since_watering,
        periodicity
      );
      return { ...plant, isMissedWatering, actualDaysUntilNextWatering };
    });

    if (wateringSortState === 'default') {
      return plantsWithSortKey; // Or just `plants` if you don't need sort keys for default display enhancements
    }

    return [...plantsWithSortKey].sort((a, b) => { // Sort a copy
      if (wateringSortState === 'urgent') {
        // Rule 1: Missed watering comes first
        if (a.isMissedWatering && !b.isMissedWatering) return -1;
        if (!a.isMissedWatering && b.isMissedWatering) return 1;

        // Rule 2: Sort by actualDaysUntilNextWatering (ascending for urgent)
        // null values (no watering schedule) go to the bottom for urgent sort
        if (a.actualDaysUntilNextWatering === null && b.actualDaysUntilNextWatering !== null) return 1;
        if (a.actualDaysUntilNextWatering !== null && b.actualDaysUntilNextWatering === null) return -1;
        if (a.actualDaysUntilNextWatering === null && b.actualDaysUntilNextWatering === null) return 0;
        
        if (a.actualDaysUntilNextWatering! < b.actualDaysUntilNextWatering!) return -1;
        if (a.actualDaysUntilNextWatering! > b.actualDaysUntilNextWatering!) return 1;
      } else if (wateringSortState === 'leastUrgent') {
        // Rule 1: Missed watering goes to the very bottom for least urgent
        if (a.isMissedWatering && !b.isMissedWatering) return 1;
        if (!a.isMissedWatering && b.isMissedWatering) return -1;
        // If both are missed or both not missed, continue to next rule

        // Rule 2: Sort by actualDaysUntilNextWatering (descending for least urgent)
        // null values (no watering schedule) go after defined schedules but before missed
        if (a.actualDaysUntilNextWatering === null && b.actualDaysUntilNextWatering !== null) return 1; 
        if (a.actualDaysUntilNextWatering !== null && b.actualDaysUntilNextWatering === null) return -1;
        if (a.actualDaysUntilNextWatering === null && b.actualDaysUntilNextWatering === null) return 0;

        // Both are not null here for actualDaysUntilNextWatering
        if (a.actualDaysUntilNextWatering! > b.actualDaysUntilNextWatering!) return -1; // Larger days (less urgent) comes first
        if (a.actualDaysUntilNextWatering! < b.actualDaysUntilNextWatering!) return 1;
      }
      return 0;
    });
  }, [plants, wateringSortState, periodicities, wateringHistory]);

  // Custom render function for each plant card
  const renderPlantCard = (plant: PlantWithSortKey) => {
    // Get the calculated periodicity or fall back to the default watering schedule
    const periodicity = periodicities[plant.name] || plant.watering_schedule;
    const calculationMethod = calculationMethods[plant.name];
    
    // Get watering history with today and next watering indicators
    const { 
      history, 
      fertilized, 
      washed, 
      neemoiled, // Existing neemoiled
      pestmixed, // Added pestmixed
      today, 
      nextWatering, 
      isMissedWatering, 
      weekdays,
      actualDaysUntilNextWatering
    } = generateWateringHistory(
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
            <div>
              <Text type="secondary" style={{ fontFamily: "'Quicksand', sans-serif" }}>
                Watering Cycle: {periodicity} days
                {calculationMethod && (
                  <Tooltip title={calculationMethod === 'mean' ? 'Simple average of all watering intervals' : 'Moving average of last 5 watering intervals'}>
                    <span style={{ 
                      marginLeft: 4, 
                      fontSize: '10px', 
                      opacity: 0.7, 
                      fontStyle: 'italic',
                      cursor: 'help',
                      padding: '1px 4px',
                      borderRadius: '3px',
                      backgroundColor: calculationMethod === 'moving_avg' ? 'rgba(24, 144, 255, 0.1)' : 'transparent'
                    }}>
                      {calculationMethod === 'mean' ? 'mean' : 'ma 5'}
                    </span>
                  </Tooltip>
                )}
              </Text>
            </div>
          </div>
          
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <div style={{ flex: 1 }}>
              <WateringHistory 
                history={history}
                fertilized={fertilized}
                washed={washed}
                neemoiled={neemoiled}
                pestmixed={pestmixed}
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
            <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
              <div style={{ width: 16, height: 16, position: 'relative', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <svg viewBox="0 0 24 24" width="16" height="16">
                   {/* Brown WashingSprayIcon for Neem Oil legend */}
                  <path d="M12,3.77L11.25,4.61C11.25,4.61 9.97,6.06 8.68,7.94C7.39,9.82 6,12.07 6,14.23A6,6 0 0,0 12,20.23A6,6 0 0,0 18,14.23C18,12.07 16.61,9.82 15.32,7.94C14.03,6.06 12.75,4.61 12.75,4.61L12,3.77M12,6.9C12.44,7.42 12.84,7.85 13.68,9.07C14.89,10.83 16,13.07 16,14.23C16,16.45 14.22,18.23 12,18.23C9.78,18.23 8,16.45 8,14.23C8,13.07 9.11,10.83 10.32,9.07C11.16,7.85 11.56,7.42 12,6.9Z" fill="#8B4513"/>
                </svg>
              </div>
              <Text type="secondary" style={{ fontSize: 12, lineHeight: 1 }}>Neem Oil</Text>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
              <div style={{ width: 16, height: 16, position: 'relative', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <svg viewBox="0 0 24 24" width="16" height="16">
                  <path d="M12,3.77L11.25,4.61C11.25,4.61 9.97,6.06 8.68,7.94C7.39,9.82 6,12.07 6,14.23A6,6 0 0,0 12,20.23A6,6 0 0,0 18,14.23C18,12.07 16.61,9.82 15.32,7.94C14.03,6.06 12.75,4.61 12.75,4.61L12,3.77M12,6.9C12.44,7.42 12.84,7.85 13.68,9.07C14.89,10.83 16,13.07 16,14.23C16,16.45 14.22,18.23 12,18.23C9.78,18.23 8,16.45 8,14.23C8,13.07 9.11,10.83 10.32,9.07C11.16,7.85 11.56,7.42 12,6.9Z" fill="#800080"/>
                </svg>
              </div>
              <Text type="secondary" style={{ fontSize: 12, lineHeight: 1 }}>Pest Mix</Text>
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
      
      <Title level={2} style={{ marginBottom: 12, fontFamily: "'Quicksand', sans-serif", fontWeight: 700, color: 'var(--color-text-primary)' }}>Plants Overview</Title>
      
      {/* Sorting Toggle Button */} 
      <div style={{ marginBottom: 24, textAlign: 'right' }}>
        <Button 
          type={wateringSortState !== 'default' ? "primary" : "default"}
          onClick={() => {
            if (wateringSortState === 'default') {
              setWateringSortState('urgent');
            } else if (wateringSortState === 'urgent') {
              setWateringSortState('leastUrgent');
            } else {
              setWateringSortState('default');
            }
          }}
          icon={
            wateringSortState === 'urgent' ? <ArrowUpOutlined /> :
            wateringSortState === 'leastUrgent' ? <ArrowDownOutlined /> :
            <FilterOutlined />
          }
        >
          Watering Need
        </Button>
      </div>
      
      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px 0' }}>
          <Text>Loading plants...</Text>
        </div>
      ) : (
        <div>
          {displayedPlants.map(renderPlantCard)}
        </div>
      )}
    </div>
  );
} 