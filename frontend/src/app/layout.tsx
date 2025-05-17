'use client'

import { Layout } from 'antd'
import { HomeOutlined, ExperimentOutlined } from '@ant-design/icons'
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
      key: '/plants/overview',
      icon: <ExperimentOutlined />,
      label: 'Plants Overview',
    },
  ]

  return (
    <html lang="en">
      <body>
        <StyledComponentsRegistry>
          <ConfigProvider>
            <Layout className="site-layout">
              <Header style={{ 
                padding: 0, 
                background: 'var(--color-card)',
                borderBottom: '1px solid var(--color-divider)',
                boxShadow: '0 2px 8px rgba(107, 86, 62, 0.05)'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', padding: '0 24px', height: '64px' }}>
                  <h1 style={{ 
                    margin: 0, 
                    marginRight: '32px', 
                    fontSize: '28px', 
                    fontFamily: "'Quicksand', sans-serif",
                    fontWeight: 700,
                    color: 'var(--color-accent-primary)'
                  }}>
                    BLUMN
                  </h1>
                  <nav>
                    <a href="/" style={{ 
                      marginRight: '24px', 
                      color: 'var(--color-text-secondary)', 
                      fontFamily: "'Open Sans', sans-serif",
                      fontSize: '15px',
                      fontWeight: 500,
                      transition: 'color 0.2s'
                    }}>Home</a>
                    <a href="/plants" style={{ 
                      marginRight: '24px', 
                      color: 'var(--color-text-secondary)',
                      fontFamily: "'Open Sans', sans-serif",
                      fontSize: '15px',
                      fontWeight: 500,
                      transition: 'color 0.2s'
                    }}>Plants</a>
                    <a href="/plants/overview" style={{ 
                      color: 'var(--color-accent-primary)',
                      fontFamily: "'Open Sans', sans-serif",
                      fontSize: '15px',
                      fontWeight: 600,
                      transition: 'color 0.2s'
                    }}>Plants Overview</a>
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