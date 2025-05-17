/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'export',  // Export static HTML
  distDir: 'out',    // Output to the 'out' directory
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
  // Make sure images work with static export
  images: {
    unoptimized: true,
  },
}

module.exports = nextConfig 