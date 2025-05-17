'use client'

import { Card, Button, Row, Col, Typography } from 'antd'
import { PlusOutlined, CalendarOutlined } from '@ant-design/icons'

const { Title } = Typography

export default function Home() {
  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
      <Title level={2}>Welcome to Blumn</Title>
      
      <Row gutter={[16, 16]}>
        <Col xs={24} md={12}>
          <Card title="Quick Actions">
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <Button type="primary" icon={<PlusOutlined />} block>
                Add Plant Care Entry
              </Button>
              <Button icon={<CalendarOutlined />} href="/plants/overview" block>
                Plants Overview
              </Button>
            </div>
          </Card>
        </Col>
        
        <Col xs={24} md={12}>
          <Card title="Recent Activity">
            <Typography.Text type="secondary">
              No recent activities to display.
            </Typography.Text>
          </Card>
        </Col>
      </Row>
    </div>
  )
} 