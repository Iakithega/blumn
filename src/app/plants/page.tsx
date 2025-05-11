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
          <Button type="link">Care History</Button>
        </Space>
      ),
    },
  ]

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
        <Table
          columns={columns}
          dataSource={plants}
          pagination={false}
          loading={loading}
        />
      </Card>
    </div>
  )
} 