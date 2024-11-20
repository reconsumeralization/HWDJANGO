import Head from 'next/head'
import { useState } from 'react'

export default function Home() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: ''
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/contact`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })
      if (res.ok) {
        alert('Message sent successfully!')
        setFormData({ name: '', email: '', phone: '', message: '' })
      }
    } catch (error) {
      console.error('Error:', error)
    }
  }

  return (
    <>
      <Head>
        <title>HW Asphalt FL | Professional Asphalt Services in Florida</title>
        <meta name="description" content="Professional asphalt services in Florida" />
      </Head>

      <main className="min-h-screen">
        {/* Hero Section */}
        <section className="bg-gray-900 text-white py-20">
          <div className="container mx-auto px-4">
            <h1 className="text-5xl font-bold mb-4">Professional Asphalt Services</h1>
            <p className="text-xl mb-8">Quality asphalt solutions in Florida</p>
            <button className="bg-yellow-500 text-black px-8 py-3 rounded-lg">
              Get a Quote
            </button>
          </div>
        </section>

        {/* Contact Form */}
        <section className="py-16">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold mb-8">Contact Us</h2>
            <form onSubmit={handleSubmit} className="max-w-lg">
              <div className="mb-4">
                <input
                  type="text"
                  placeholder="Name"
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full p-2 border rounded"
                  required
                />
              </div>
              {/* Add other form fields */}
            </form>
          </div>
        </section>
      </main>
    </>
  )
}
