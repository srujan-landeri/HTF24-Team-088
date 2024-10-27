// UserLikes.jsx
import React, { useState, useEffect } from 'react';
import ArticleList from './ArticleList';
import { Search } from 'lucide-react';
import { toast } from 'react-toastify';

const UserLikes = ({setPage}) => {
    const [searchQuery, setSearchQuery] = useState('');
    const [articles, setArticles] = useState([]);
    const userId = localStorage.getItem('userId') || '671d663c60819ecd6a91e985';
    useEffect(() => {
        fetchLikedArticles();
    }, []);

    const fetchLikedArticles = async () => {
        try {
            // First, get all liked article IDs
            const response = await fetch(`http://localhost:8000/likes/${userId}`);
            const data = await response.json();
            
            // Fetch details for each article ID
            const articleDetails = await Promise.all(
                data.liked_articles.map(async (articleId) => {
                    const detailsResponse = await fetch(`http://localhost:8000/articles/details/${articleId}`);
                    const details = await detailsResponse.json();
                    return details;
                })
            );
            setArticles(articleDetails);
        } catch (error) {
            console.error('Error fetching liked articles:', error);
            toast({
                variant: "destructive",
                description: "Failed to fetch liked articles",
                duration: 2000,
            });
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
                    author: article.author
                }),
            });

            if (!response.ok) throw new Error('Failed to like article');
            // Refresh the list after liking/unliking
            fetchLikedArticles();
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
                    author: article.author
                }),
            });
            if (!response.ok) throw new Error('Failed to dislike article');
            fetchLikedArticles();
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
                    author: article.author
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
        article.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        article.description.toLowerCase().includes(searchQuery.toLowerCase())
    );

    function handleSearch(e) {
        e.preventDefault();
    }

    return (
        <div className="min-h-screen bg-gray-50">
            <header className="sticky top-0 bg-white border-b border-gray-200 shadow-sm">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                    <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                        <div className="flex items-center">
                            <h1 className="text-2xl font-bold text-gray-900 tracking-tight">
                                Liked Articles
                            </h1>
                        </div>

                        <form
                            onSubmit={handleSearch}
                            className="flex-1 max-w-2xl md:mx-4"
                        >
                            <div className="relative">
                                <input
                                    type="text"
                                    placeholder="Search liked articles..."
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

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {
                    filteredArticles.length > 0 ? <ArticleList
                        articles={filteredArticles}
                        onLike={handleLike}
                        onDislike={handleDislike}
                        onCopyLink={handleCopyLink}
                        onSave={handleSave}
                    /> : 
                    <div className="text-center text-gray-500 mt-40 flex justify-center flex-col">
                        <h1 className='text-3xl'>No liked articles found </h1>
                        <button className='block text-2xl text-center text-blue-500 hover:text-blue-600' onClick={() => setPage('explorer')}> 
                            Explore News Articles Now
                        </button>
                    </div>
                }
            </main>
        </div>
    );
};

export default UserLikes;