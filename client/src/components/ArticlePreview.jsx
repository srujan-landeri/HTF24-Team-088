import React from 'react';
import { ExternalLink } from 'lucide-react';

const LinkPreview = ({ article, embedData }) => {
  if(!embedData) {
    return null;
  }
  
  const handleClick = () => {
    if (article.url) {
      window.open(article.url, '_blank', 'noopener,noreferrer');
    }
  };

  // Default image URL for cases with no image available
  const defaultImage = 'https://via.placeholder.com/600x400?text=No+Image+Available';

  return (
    <div className="w-max-5xl mx-auto">
      <div 
        onClick={handleClick}
        className="relative group cursor-pointer border border-gray-200 rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300"
      >
        {/* Image Container */}
        <div className="relative overflow-hidden bg-gray-100">
          <img 
            src={embedData?.image || defaultImage}  // Use default image if no embedData image
            alt={embedData?.title || article.title}
            className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
          />

        
        </div>

        {/* Link Preview Info */}
        <div className="p-2 bg-gray-50 border-t border-gray-100">
          <div className="flex items-center gap-2">
            {embedData?.favicon && (
              <img 
                src={embedData.favicon} 
                alt="" 
                className="w-3 h-3"
              />
            )}
            <span className="text-xs text-gray-500 truncate">
              {article.url ? new URL(article.url).hostname : 'Read more'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LinkPreview;
