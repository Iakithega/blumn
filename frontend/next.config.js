/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NODE_ENV === 'production' 
          ? '/api/:path*'  // In production, forward to the same server
          : 'http://localhost:8000/api/:path*', // In development, forward to the backend server
      },
    ]
  },
  output: 'export',
}

module.exports = nextConfig 