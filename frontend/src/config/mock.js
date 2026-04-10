export const MOCK_MODE = String(import.meta.env.VITE_MOCK_MODE || 'false').toLowerCase() === 'true'

export const DEMO_LECTURE_ID = 'demo-lecture'

export function createMockLecture(lectureId = DEMO_LECTURE_ID) {
  const slides = [
    {
      heading: 'Welcome to AI Learning',
      summary: 'An overview of how AI can accelerate understanding and retention.',
      important_points: ['Fast summaries', 'Personalized pacing', 'Interactive explanation'],
      script: 'Welcome to your AI-powered class. We will walk through the core ideas in a structured flow.',
      audio_url: '/sample.mp3',
      slide_url: '/faq.png',
    },
    {
      heading: 'Core Concepts',
      summary: 'Breaking complex topics into concise conceptual chunks.',
      important_points: ['Chunking', 'Context windows', 'Progressive disclosure'],
      script: 'Core concepts are introduced in manageable chunks so learners can keep cognitive load low.',
      audio_url: '/sample.mp3',
      slide_url: '/homechar.png',
    },
    {
      heading: 'Practice and Recall',
      summary: 'Use flashcards, mini tests, and repetition to improve retention.',
      important_points: ['Retrieval practice', 'Spaced repetition', 'Feedback loops'],
      script: 'Practice and recall loops are what turn passive reading into active long-term understanding.',
      audio_url: '/sample.mp3',
      slide_url: '/faq.png',
    },
  ]

  return {
    lecture_title: `Mock Lecture ${lectureId}`,
    slides,
  }
}

export function createMockPodcast(slideContent = '', slideIndex = 0) {
  const text = String(slideContent || 'This is a mock podcast segment for frontend-only development.').trim()
  const midpoint = Math.max(1, Math.floor(text.length / 2))

  return {
    audio_url: '/sample.mp3',
    dialogue: [
      { speaker: 'ziva', text: text.slice(0, midpoint) || 'Let us begin this section.' },
      { speaker: 'zyro', text: text.slice(midpoint) || 'Great, now let us summarize key takeaways.' },
    ],
    timings: [
      { start: 0, end: 4, speaker: 'ziva' },
      { start: 4, end: 8, speaker: 'zyro' },
    ],
    status: 'partial',
    slide_index: slideIndex,
  }
}
