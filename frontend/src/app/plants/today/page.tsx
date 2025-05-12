'use client';
import React, { useEffect, useState } from 'react';
import { Table } from 'antd';

interface Plant {
  id: number;
  name: string;
  last_watered: string | null;
  last_fertilized: string | null;
  days_since_watering: number | null;
  days_since_fertilizing: number | null;
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
};

function getImageSrc(plantName: string) {
  const base = plantName
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9 ]/g, '')
    .replace(/\s+/g, '_');
  console.log('Normalized:', base, 'Mapped to:', imageMap[base]);
  if (imageMap[base]) {
    return `/plant_images/${imageMap[base]}`;
  }
  return '/plant_images/default.jpg';
}

const columns = [
  {
    title: 'Image',
    dataIndex: 'name',
    key: 'image',
    render: (name: string) => (
      <img
        src={getImageSrc(name)}
        alt={name}
        style={{ width: 60, height: 60, objectFit: 'cover', borderRadius: 8 }}
      />
    ),
  },
  { title: 'Plant Name', dataIndex: 'name', key: 'name' },
  {
    title: 'Last Watered',
    dataIndex: 'last_watered',
    key: 'last_watered',
    render: (_: any, record: Plant) =>
      record.last_watered
        ? `${record.last_watered} (${record.days_since_watering} days ago)`
        : 'never',
  },
  {
    title: 'Last Fertilized',
    dataIndex: 'last_fertilized',
    key: 'last_fertilized',
    render: (_: any, record: Plant) =>
      record.last_fertilized
        ? `${record.last_fertilized} (${record.days_since_fertilizing} days ago)`
        : 'never',
  },
];

export default function TodayPlants() {
  const [plants, setPlants] = useState<Plant[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/plants/today')
      .then(res => res.json())
      .then(data => {
        setPlants(data);
        setLoading(false);
      });
  }, []);

  return (
    <div>
      <h1>Today's Plants</h1>
      <Table
        columns={columns}
        dataSource={plants}
        rowKey="id"
        loading={loading}
        pagination={false}
      />
    </div>
  );
} 