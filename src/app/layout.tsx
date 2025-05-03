import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Blumn - Plant Care Tracker',
  description: 'Track and manage your plant care routine',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <nav className="bg-green-600 text-white p-4">
          <div className="container mx-auto flex justify-between items-center">
            <h1 className="text-xl font-bold">Blumn</h1>
            <div className="space-x-4">
              <a href="/" className="hover:text-green-200">Home</a>
              <a href="/plants" className="hover:text-green-200">Plants</a>
              <a href="/care-history" className="hover:text-green-200">Care History</a>
            </div>
          </div>
        </nav>
        <main className="container mx-auto p-4">
          {children}
        </main>
      </body>
    </html>
  )
} 