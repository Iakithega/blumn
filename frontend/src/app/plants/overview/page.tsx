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

// Helper function to create a dummy watering history (since the real data would come from the API)
function generateWateringHistory(daysAgo: number | null, schedule: number): boolean[] {
  const days = 30; // Show last 30 days
  const history: boolean[] = Array(days).fill(false);
  
  if (daysAgo === null || daysAgo > days) return history;
  
  // Mark the last watering day
  history[days - 1 - daysAgo] = true;
  
  // Mark previous watering days based on schedule
  for (let i = days - 1 - daysAgo; i >= 0; i -= schedule) {
    if (i >= 0) history[i] = true;
  }
  
  return history;
}

// Component for rendering watering history visualization
function WateringHistory({ history }: { history: boolean[] }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '3px', height: '32px', width: '100%' }}>
      {history.map((watered, i) => (
        <Tooltip key={i} title={`${30 - i} days ago: ${watered ? 'Watered' : 'Not watered'}`}>
          <div
            style={{
              width: '100%',
              height: '32px',
              backgroundColor: watered ? '#52c41a' : '#f0f0f0',
              borderRadius: '3px',
              flexGrow: 1,
              flexBasis: 0,
            }}
          />
        </Tooltip>
      ))}
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

  useEffect(() => {
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
  }, []);

  // Custom render function for each plant card
  const renderPlantCard = (plant: Plant) => {
    const history = generateWateringHistory(plant.days_since_watering, plant.watering_schedule);
    
    return (
      <Card 
        key={plant.id} 
        style={{ marginBottom: 24 }}
        bodyStyle={{ padding: 20 }}
      >
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
            
            <Divider style={{ margin: '16px 0' }} />
            
            {/* Watering History */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 12 }}>
                <Text strong style={{ fontSize: 16 }}>Watering History (Last 30 Days)</Text>
                <Text type="secondary">Recommended: Every {plant.watering_schedule} days</Text>
              </div>
              
              <div style={{ display: 'flex', alignItems: 'center', margin: '0 -16px' }}>
                <Text type="secondary" style={{ width: '40px', textAlign: 'center' }}>30d ago</Text>
                <div style={{ flex: 1, padding: '0 12px' }}>
                  <WateringHistory history={history} />
                </div>
                <Text type="secondary" style={{ width: '40px', textAlign: 'center' }}>Today</Text>
              </div>
            </div>
          </Col>
        </Row>
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