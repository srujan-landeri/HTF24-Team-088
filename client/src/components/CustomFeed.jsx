import React, { useState } from 'react';
import { Search } from 'lucide-react';

const FeedPage = () => {
  const [selectedTags, setSelectedTags] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');

  const tags = [
    { id: 'ai', label: 'ai' },
    { id: 'architecture', label: 'architecture' },
    { id: 'cloud', label: 'cloud' },
    { id: 'crypto', label: 'crypto' },
    { id: 'database', label: 'database' },
    { id: 'data-science', label: 'data-science' },
    { id: 'devops', label: 'devops' },
    { id: 'elixir', label: 'elixir' },
    { id: 'gaming', label: 'gaming' },
    { id: 'golang', label: 'golang' },
    { id: 'java', label: 'java' },
    { id: 'javascript', label: 'javascript' },
    { id: 'machine-learning', label: 'machine-learning' },
    { id: 'mobile', label: 'mobile' },
    { id: '.net', label: '.net' },
    { id: 'open-source', label: 'open-source' },
    { id: 'python', label: 'python' },
    { id: 'react', label: 'react' },
    { id: 'ruby', label: 'ruby' },
    { id: 'rust', label: 'rust' },
    { id: 'security', label: 'security' },
    { id: 'tech-news', label: 'tech-news' },
    { id: 'testing', label: 'testing' },
    { id: 'tools', label: 'tools' },
    { id: 'webdev', label: 'webdev' }
  ];

  const toggleTag = (tagId) => {
    setSelectedTags(prev =>
      prev.includes(tagId)
        ? prev.filter(id => id !== tagId)
        : [...prev, tagId]
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="transition-all duration-200 ease-in-out 
                      ml-0 lg:ml-56 
                      pt-4 sm:pt-6 lg:pt-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Search Bar */}
          <div className="relative mb-6 sm:mb-8">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              className="block w-full pl-10 pr-3 py-2 sm:py-3
                         border border-gray-200 
                         rounded-lg
                         bg-white 
                         text-gray-900 
                         placeholder-gray-500
                         shadow-sm
                         transition-colors
                         focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent
                         hover:border-gray-300"
              placeholder="Search javascript, php, git, etc..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          {/* Tags Section */}
          <div className="space-y-6">
            <div className="flex flex-wrap gap-2">
              {tags.map((tag) => (
                <button
                  key={tag.id}
                  onClick={() => toggleTag(tag.id)}
                  className={`px-3 sm:px-4 py-1.5 sm:py-2 
                             rounded-lg text-sm font-medium 
                             transition-all duration-200 
                             transform hover:scale-105
                             shadow-md hover:shadow-lg
                             active:shadow-sm active:scale-95
                             ${
                               selectedTags.includes(tag.id)
                                 ? 'bg-blue-600 text-white shadow-blue-100 hover:shadow-blue-200 hover:bg-blue-700'
                                 : 'bg-white text-gray-700 border border-gray-100 hover:border-gray-200 hover:bg-gray-50 shadow-gray-100 hover:shadow-gray-200'
                             }`}
                >
                  {tag.label}
                </button>
              ))}
            </div>

          </div>
        </div>
      </div>
    </div>
  );
};

export default FeedPage;