'use client'

import { Layout } from 'antd'
import { HomeOutlined, ExperimentOutlined, HistoryOutlined } from '@ant-design/icons'
import './globals.css'
import { ConfigProvider } from 'antd'
import StyledComponentsRegistry from './registry'

const { Header, Content } = Layout

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const menuItems = [
    {
      key: '/',
      icon: <HomeOutlined />,
      label: 'Home',
    },
    {
      key: '/plants',
      icon: <ExperimentOutlined />,
      label: 'Plants',
    },
    {
      key: '/care-history',
      icon: <HistoryOutlined />,
      label: 'Care History',
    },
  ]

  return (
    <html lang="en">
      <body>
        <StyledComponentsRegistry>
          <ConfigProvider>
            <Layout className="site-layout">
              <Header style={{ padding: 0, background: '#fff' }}>
                <div style={{ display: 'flex', alignItems: 'center', padding: '0 24px' }}>
                  <h1 style={{ margin: 0, marginRight: '24px', fontSize: '20px', color: '#1890ff' }}>
                    Blumn
                  </h1>
                  <nav>
                    <a href="/" style={{ marginRight: '20px' }}>Home</a>
                    <a href="/plants" style={{ marginRight: '20px' }}>Plants</a>
                    <a href="/care-history">Care History</a>
                  </nav>
                </div>
              </Header>
              <Content className="site-content">
                {children}
              </Content>
            </Layout>
          </ConfigProvider>
        </StyledComponentsRegistry>
      </body>
    </html>
  )
} 