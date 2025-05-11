'use client'

import React from 'react'
import { createCache, StyleProvider } from '@ant-design/cssinjs'
import { useServerInsertedHTML } from 'next/navigation'

export default function StyledComponentsRegistry({
  children,
}: {
  children: React.ReactNode
}) {
  const [cache] = React.useState(() => createCache())

  useServerInsertedHTML(() => {
    return (
      <style
        id="antd"
        dangerouslySetInnerHTML={{
          __html: Object.values(cache.cache).join(''),
        }}
      />
    )
  })

  return <StyleProvider cache={cache}>{children}</StyleProvider>
} 