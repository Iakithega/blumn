'use client';
import React, { useEffect, useState } from 'react';
import { Table, Card, Row, Col, Typography, Tooltip, Divider } from 'antd';

const { Title, Text } = Typography;

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

// Additional interface for watering history data
interface WateringHistoryData {
  plant_name: string;
  watering_dates: string[]; // Array of dates when the plant was watered
}

// Helper function to create a realistic watering history from actual data including future predictions
function generateWateringHistory(plantName: string, wateringHistory: WateringHistoryData[], daysAgo: number | null, periodicity: number): {history: boolean[], today: number, nextWatering: number} {
  const pastDays = 30; // Show last 30 days
  const futureDays = 10; // Show next 10 days
  const totalDays = pastDays + futureDays;
  const history: boolean[] = Array(totalDays).fill(false);
  
  // Find watering history for this specific plant
  const plantHistory = wateringHistory.find(h => h.plant_name === plantName);
  
  // Calculate today's position in the array
  const todayIndex = pastDays - 1;
  
  // Default value for next watering (if we can't calculate it)
  let nextWateringIndex = -1;
  
  if (!plantHistory) return { history, today: todayIndex, nextWatering: nextWateringIndex };

  // Get today's date
  const today = new Date();
  
  // Convert watering dates to Date objects
  const wateringDates = plantHistory.watering_dates.map(dateStr => {
    const parts = dateStr.split('.');
    return new Date(parseInt(parts[2]), parseInt(parts[1]) - 1, parseInt(parts[0]));
  });
  
  // Sort dates in ascending order
  wateringDates.sort((a, b) => a.getTime() - b.getTime());
  
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
    }
  }
  
  // Calculate next watering date based on periodicity and most recent watering
  if (wateringDates.length > 0 && periodicity > 0) {
    // Get the most recent watering date
    const lastWatering = wateringDates[wateringDates.length - 1];
    
    // Calculate days since last watering
    const daysSinceLastWatering = Math.floor((today.getTime() - lastWatering.getTime()) / (1000 * 60 * 60 * 24));
    
    // Calculate days until next watering
    const daysUntilNextWatering = periodicity - (daysSinceLastWatering % periodicity);
    
    // If next watering is within our future window, mark it
    if (daysUntilNextWatering <= futureDays) {
      nextWateringIndex = todayIndex + daysUntilNextWatering;
    }
  }
  
  return { history, today: todayIndex, nextWatering: nextWateringIndex };
}

// Component for rendering watering history visualization
function WateringHistory({ history, today, nextWatering }: { history: boolean[], today: number, nextWatering: number }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '3px', height: '50px', width: '100%' }}>
      {history.map((watered, i) => {
        let style = {
          width: '100%',
          height: '50px',
          backgroundColor: watered ? '#52c41a' : '#f0f0f0',
          borderRadius: '3px',
          flexGrow: 1,
          flexBasis: 0,
          border: 'none'
        };
        
        // Today's marker (black/gray outline)
        if (i === today) {
          style = {
            ...style,
            border: '2px solid #333',
            backgroundColor: '#f0f0f0'
          };
        }
        
        // Next watering marker (green outline)
        if (i === nextWatering) {
          style = {
            ...style,
            border: '2px solid #52c41a',
            backgroundColor: '#f0f0f0'
          };
        }
        
        // Watering in the past
        if (watered) {
          style = {
            ...style,
            backgroundColor: '#52c41a',
            border: 'none'
          };
        }
        
        // Calculate the date for this position
        const totalDays = history.length;
        const pastDays = today + 1;
        const daysFromToday = i - today;
        
        let tooltipDate = new Date();
        tooltipDate.setDate(tooltipDate.getDate() + daysFromToday);
        const tooltipText = i < today ? 
          `${Math.abs(daysFromToday)} days ago: ${watered ? 'Watered' : 'Not watered'}` : 
          i === today ? 
            'Today' : 
            i === nextWatering ? 
              `${daysFromToday} days from now: Next watering` : 
              `${daysFromToday} days from now`;
        
        return (
          <Tooltip key={i} title={tooltipText}>
            <div style={style} />
          </Tooltip>
        );
      })}
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
    // Fetch plants data
    fetch('http://127.0.0.1:8000/api/plants/today')
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
    
    // Fetch watering periodicity data
    fetch('http://127.0.0.1:8000/api/plants/periodicity')
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

    // Fetch raw plant data to extract watering history
    fetch('http://127.0.0.1:8000/api/plants')
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          // Process the data to extract watering dates for each plant
          const plantWateringMap: Record<string, string[]> = {};
          
          data.data.forEach((entry: any) => {
            const plantName = entry['plant name'];
            const date = entry.date;
            const daysWithoutWater = entry['days without water'];
            const waterEntry = entry.water;
            
            // Check if this row indicates a watering event
            const isWateringEvent = 
              daysWithoutWater === 0 || 
              (typeof daysWithoutWater === 'string' && daysWithoutWater.trim() === '0') || 
              waterEntry;
              
            if (plantName && date && isWateringEvent) {
              if (!plantWateringMap[plantName]) {
                plantWateringMap[plantName] = [];
              }
              plantWateringMap[plantName].push(date);
            }
          });
          
          // Convert to array format for state
          const wateringHistoryData = Object.entries(plantWateringMap).map(([plant_name, watering_dates]) => ({
            plant_name,
            watering_dates
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
    const { history, today, nextWatering } = generateWateringHistory(
      plant.name, 
      wateringHistory, 
      plant.days_since_watering,
      periodicity
    );
    
    return (
      <Card 
        key={plant.id} 
        style={{ marginBottom: 24 }}
        bodyStyle={{ padding: 20 }}
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
                borderRadius: 8,
                marginBottom: 8 
              }}
            />
          </Col>
          
          {/* Right column - Plant Info */}
          <Col xs={24} sm={18} md={20}>
            <div style={{ marginBottom: 16 }}>
              <Title level={4} style={{ marginBottom: 12 }}>{plant.name}</Title>
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
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 12 }}>
            <Text strong style={{ fontSize: 16 }}>Watering History & Forecast</Text>
            <Text type="secondary">Watering Cycle: {periodicity} days</Text>
          </div>
          
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <Text type="secondary" style={{ width: '50px', textAlign: 'center' }}>30d ago</Text>
            <div style={{ flex: 1, padding: '0 12px' }}>
              <WateringHistory history={history} today={today} nextWatering={nextWatering} />
            </div>
            <Text type="secondary" style={{ width: '50px', textAlign: 'center' }}>+10d</Text>
          </div>
          
          {/* Legend */}
          <div style={{ marginTop: 12, display: 'flex', gap: 16, justifyContent: 'flex-end' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
              <div style={{ width: 16, height: 16, backgroundColor: '#52c41a', borderRadius: 2 }}></div>
              <Text type="secondary" style={{ fontSize: 12 }}>Past Watering</Text>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
              <div style={{ width: 16, height: 16, border: '2px solid #333', borderRadius: 2 }}></div>
              <Text type="secondary" style={{ fontSize: 12 }}>Today</Text>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
              <div style={{ width: 16, height: 16, border: '2px solid #52c41a', borderRadius: 2 }}></div>
              <Text type="secondary" style={{ fontSize: 12 }}>Next Watering</Text>
            </div>
          </div>
        </div>
      </Card>
    );
  };

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '0 16px' }}>
      <Title level={2}>Plant Overview</Title>
      
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