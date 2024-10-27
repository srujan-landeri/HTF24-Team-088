import React, { useState, useEffect } from 'react';
import ArticleList from './ArticleList';
import { ThumbsUp, ThumbsDown, MessageSquare, Bookmark, Link2, Search } from 'lucide-react';
import { toast, ToastContainer } from 'react-toastify';
import data from "../data/sample_data.json"
import {InfinitySpin} from 'react-loader-spinner';

// Explore component
const Explore = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [articles, setArticles] = useState([]);
    const [loading, setLoading] = useState(false);

    const userId = localStorage.getItem('userId') || '671d663c60819ecd6a91e985';

    useEffect(() => {
            // Combine business and sports articles
            setLoading(true);
            const combinedArticles = [
                ...data.articles.business.links.map((link, index) => ({
                    url: link,
                    title: data.articles.business.titles[index],
                    source: data.articles.business.sources[index],
                    published_at: data.articles.business.published_dates[index],
                    description: data.articles.business.descriptions[index],
                    category: 'business'
                })),
                ...data.articles.sports.links.map((link, index) => ({
                    url: link,
                    title: data.articles.sports.titles[index],
                    source: data.articles.sports.sources[index],
                    published_at: data.articles.sports.published_dates[index],
                    description: data.articles.sports.descriptions[index],
                    category: 'sports'
                }))
            ];

            setTimeout(() => {
                setArticles(combinedArticles);
                setLoading(false);
            }, 2000);    
        }, []);

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
        setArticles(data);
        console.log(data);
      } catch (error) {
        console.error('Error fetching news:', error);
      }
    };


    const handleLike = async (article) => {
        try {
            const response = await fetch('http://localhost:8000/articles/like', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: userId,
                    article_url: article.url,
                    title: article.title,
                    source: article.source,
                    published_at: article.published_at,
                    description: article.description,
                    author: article.source
                }),
            });

            if (!response.ok) throw new Error('Failed to like article');
        } catch (error) {
            console.error('Error liking article:', error);
        }
    };

    const handleDislike = async (article) => {
        try {
            const response = await fetch('http://localhost:8000/articles/dislike', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: userId,
                    article_url: article.url,
                    title: article.title,
                    source: article.source,
                    published_at: article.published_at,
                    description: article.description,
                    author: article.source
                }),
            });
            if (!response.ok) throw new Error('Failed to dislike article');
        } catch (error) {
            console.error('Error disliking article:', error);
        }
    };

    const handleSave = async (article) => {
        try {
            const response = await fetch('http://localhost:8000/articles/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: userId,
                    article_url: article.url,
                    title: article.title,
                    source: article.source,
                    published_at: article.published_at,
                    description: article.description,
                    author: article.source
                }),
            });

            if (!response.ok) throw new Error('Failed to save article');
        } catch (error) {
            console.error('Error saving article:', error);
            toast.error('Failed to save article');
        }
    };

    // New handler for copying link to clipboard
    const handleCopyLink = async (url) => {
        try {
            await navigator.clipboard.writeText(url);
        } catch (error) {
            console.error('Error copying link:', error);
        }
    };

    const filteredArticles = articles.filter(article =>
        article.title.includes(searchQuery) ||
        article.description.includes(searchQuery)
    );

    function handleSearch(e) {
        e.preventDefault();
        setArticles(filteredArticles)
    }

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="sticky top-0 z-10 bg-white border-b border-gray-200 shadow-sm">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                        {/* Logo and Title Section */}
                        <div className="flex items-center">
                            <h1 className="text-2xl font-bold text-gray-900 tracking-tight">
                                Explore News
                            </h1>
                        </div>

                        {/* Search Section */}
                        <form
                            onSubmit={handleSearch}
                            className="flex-1 max-w-2xl md:mx-4"
                        >
                            <div className="relative">
                                <input
                                    type="text"
                                    placeholder="Search news articles..."
                                    className="w-full pl-4 pr-12 py-2.5 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-200 ease-in-out"
                                    value={searchQuery}
                                    onChange={(e) => setSearchQuery(e.target.value)}
                                />
                                <button
                                    type="submit"
                                    variant="ghost"
                                    size="icon"
                                    className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                                >
                                    <Search className="h-5 w-5" />
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </header>

            {/* Main content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

                {!loading && <ArticleList
                    articles={filteredArticles}
                    onLike={handleLike}
                    onDislike={handleDislike}
                    onCopyLink={handleCopyLink}
                    onSave={handleSave}
                />}
                {
                  loading &&  <div className='h-[85vh] flex justify-center items-center'>
                        <InfinitySpin
                            visible={true}
                            width="200"
                            color="#4fa94d"
                            ariaLabel="infinity-spin-loading"
                        />
                    </div>
                }
            </main>
        </div>
    );
};

export default Explore;
