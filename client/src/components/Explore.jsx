import React, { useState, useEffect } from 'react';
import ArticleList from './ArticleList';
import { ThumbsUp, ThumbsDown, MessageSquare, Bookmark, Link2, Search } from 'lucide-react';
import { toast } from 'react-toastify';

// Explore component
const Explore = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [articles, setArticles] = useState([]);
    const userId = localStorage.getItem('userId') || '671d663c60819ecd6a91e985';

    useEffect(() => {
        const url = 'http://localhost:8000/aggregated_news_normal';
        const requestData = {
            categories: [
                'business', 
                'entertainment', 
                'health', 
                'science', 
                'sports', 
                'technology'
            ],
            language: 'en' // Optional, you can remove or change the language as needed
        };

        const fetchData = async () => {
            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestData)
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const res = await response.json();
                console.log('Aggregated News:', res);

                const combinedArticles = requestData.categories.flatMap(category => {
                    const categoryData = res[category];
                    if (!categoryData || !categoryData.links) {
                        return []; // Skip if the category data is not available
                    }

                    return categoryData.links.map((link, index) => ({
                        url: link || '', // Fallback to an empty string if link is null/undefined
                        title: (categoryData.titles && categoryData.titles[index]) || '', // Use the index to get the correct title
                        source: (categoryData.sources && categoryData.sources[index]) || '', // Use the index to get the correct source
                        published_at: (categoryData.published_dates && categoryData.published_dates[index]) || '', // Use the index to get the correct date
                        description: (categoryData.descriptions && categoryData.descriptions[index]) || '', // Use the index to get the correct description
                        category
                    }));
                });

                setArticles(combinedArticles);
                console.log('Articles:', combinedArticles);
            } catch (error) {
                console.error('Error fetching aggregated news:', error);
            }
        };

        fetchData();
    }, []); // Empty dependency array means this effect runs once when the component mounts

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
            toast({
                description: "Article saved successfully",
                duration: 2000,
            });
        } catch (error) {
            console.error('Error saving article:', error);
            toast({
                variant: "destructive",
                description: "Failed to save article",
                duration: 2000,
            });
        }
    };

    // New handler for copying link to clipboard
    const handleCopyLink = async (article) => {
        try {
            await navigator.clipboard.writeText(article.url);
            toast({
                description: "Link copied to clipboard",
                duration: 2000,
            });
        } catch (error) {
            console.error('Error copying link:', error);
            toast({
                variant: "destructive",
                description: "Failed to copy link",
                duration: 2000,
            });
        }
    };

    const filteredArticles = articles.filter(article =>
        article.title.includes(searchQuery) ||
        article.description.includes(searchQuery)
    );

    function handleSearch(e) {
        e.preventDefault();
    }

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="sticky top-0 bg-white border-b border-gray-200 shadow-sm">
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

                        {/* Additional Actions */}
                        <div className="flex items-center space-x-4">
                            <button variant="outline" className="hidden md:inline-flex">
                                Categories
                            </button>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

                <ArticleList
                    articles={filteredArticles}
                    onLike={handleLike}
                    onDislike={handleDislike}
                    onCopyLink={handleCopyLink}
                    onSave={handleSave}
                />
            </main>
        </div>
    );
};

export default Explore;
