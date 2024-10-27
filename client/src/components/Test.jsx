import React, { useEffect, useState } from 'react';

const Test = () => {
  const [news, setNews] = useState([]);
    const fetchNews = async () => {
      try {
        const response = await fetch('http://localhost:8000/aggregated_news_normal', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            categories: ['business', 'entertainment', 'health', 'science', 'sports', 'technology'],
            language: 'en'
          }),
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log(data)
        setNews(data);
      } catch (error) {
        console.error('Error fetching news:', error);
      }
    };

  return (
    <div className='mt-40'>
      <h1>Aggregated News</h1>
      {/* Render your news data here */}
      <button onClick={fetchNews}>Fetch News</button>
      <pre>{JSON.stringify(news, null, 2)}</pre>
    </div>
  );
};

export default Test;
