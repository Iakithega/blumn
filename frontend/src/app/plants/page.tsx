'use client'

import { Table, Card, Button, Space, message } from 'antd'
import { PlusOutlined } from '@ant-design/icons'
import { useState, useEffect } from 'react'

interface Plant {
  key: string
  date: string
  plant_name: string
  days_without_water: string
  water: string
  fertilizer: string
  wash: string
  size: string
}

export default function PlantsPage() {
  const [plants, setPlants] = useState<Plant[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchPlants()
  }, [])

  const fetchPlants = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/plants')
      const data = await response.json()
      
      if (data.status === 'success') {
        // Ensure data.data is an array before proceeding
        if (!Array.isArray(data.data)) {
          console.error('Expected array but got:', data.data);
          message.error('Received invalid data format from server');
          setPlants([]);
          return;
        }
        
        // Transform the data to match our interface
        const transformedData = data.data.map((plant: any, index: number) => ({
          key: index.toString(),
          date: plant.date || '',
          plant_name: plant['plant name'] || 'Unknown Plant',
          days_without_water: plant['days without water'] || '',
          water: plant.water || '',
          fertilizer: plant.fertilizer || '',
          wash: plant.wash || '',
          size: plant.size || '',
        }))
        setPlants(transformedData)
      } else {
        message.error('Failed to load plants')
      }
    } catch (error) {
      message.error('Error connecting to the server')
      console.error('Error fetching plants:', error)
    } finally {
      setLoading(false)
    }
  }

  const columns = [
    {
      title: 'Date',
      dataIndex: 'date',
      key: 'date',
    },
    {
      title: 'Plant Name',
      dataIndex: 'plant_name',
      key: 'plant_name',
    },
    {
      title: 'Days Without Water',
      dataIndex: 'days_without_water',
      key: 'days_without_water',
    },
    {
      title: 'Water',
      dataIndex: 'water',
      key: 'water',
    },
    {
      title: 'Fertilizer',
      dataIndex: 'fertilizer',
      key: 'fertilizer',
    },
    {
      title: 'Wash',
      dataIndex: 'wash',
      key: 'wash',
    },
    {
      title: 'Size',
      dataIndex: 'size',
      key: 'size',
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: unknown, record: Plant) => (
        <Space>
          <Button type="link">Edit</Button>
        </Space>
      ),
    },
  ]

  // Create a function to apply alternating row colors based on date
  const rowClassName = (record: Plant, index: number): string => {
    // Track the date groups to apply different colors
    if (index === 0) return 'even-date-row';
    
    // If the date is different from the previous row, change the color group
    const prevRecord = plants[index - 1];
    if (prevRecord && prevRecord.date !== record.date) {
      // Get the previous row's class
      const prevClass: string = rowClassName(prevRecord, index - 1);
      // Return the opposite class
      return prevClass === 'even-date-row' ? 'odd-date-row' : 'even-date-row';
    }
    
    // If same date as previous row, use the same color
    return rowClassName(plants[index - 1], index - 1);
  };

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
      <Card
        title="My Plants"
        extra={
          <Button type="primary" icon={<PlusOutlined />}>
            Add Plant
          </Button>
        }
      >
        <style jsx global>{`
          .even-date-row {
            background-color: #ffffff;
          }
          .odd-date-row {
            background-color: #f5f5f5;
          }
          .ant-table-tbody > tr.even-date-row:hover > td,
          .ant-table-tbody > tr.odd-date-row:hover > td {
            background-color: #e6f7ff !important;
          }
        `}</style>
        <Table
          columns={columns}
          dataSource={plants}
          pagination={false}
          loading={loading}
          rowClassName={rowClassName}
        />
      </Card>
    </div>
  )
} 