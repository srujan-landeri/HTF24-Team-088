import { ThumbsUp, ThumbsDown, MessageSquare, Bookmark, Link2, Search } from 'lucide-react';


// ArticleCard component
export default function ArticleCard ({ article, onLike, onDislike }){
    console.log(article)
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center space-x-3 mb-4">
        <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
          {article.source?.charAt(0).toUpperCase()}
        </div>
        <div className="flex-1">
          <div className="flex items-center justify-between">
            <h3 className="font-medium text-gray-900">{article.source}</h3>
            <span className="text-sm text-gray-500">#{article.category}</span>
          </div>
          <p className="text-sm text-gray-500">{new Date(article.published_at).toLocaleDateString()}</p>
        </div>
      </div>
      
      <h2 className="text-xl font-semibold mb-3">{article.title}</h2>
      <p className="text-gray-600 mb-4">{article.description}</p>
      
      <div className="flex items-center justify-between pt-4 border-t border-gray-100">
        <div className="flex items-center space-x-6">
          <button onClick={() => onLike(article)} className="flex items-center space-x-2 text-gray-500 hover:text-blue-500">
            <ThumbsUp className="h-5 w-5" />
            <span>0</span>
          </button>
          <button onClick={() => onDislike(article)} className="flex items-center space-x-2 text-gray-500 hover:text-red-500">
            <ThumbsDown className="h-5 w-5" />
            <span>0</span>
          </button>
          <button className="flex items-center space-x-2 text-gray-500 hover:text-gray-700">
            <MessageSquare className="h-5 w-5" />
            <span>0</span>
          </button>
        </div>
        <div className="flex items-center space-x-4">
          <button className="text-gray-500 hover:text-gray-700">
            <Bookmark className="h-5 w-5" />
          </button>
          <button className="text-gray-500 hover:text-gray-700">
            <Link2 className="h-5 w-5" />
          </button>
        </div>
      </div>
    </div>
  );
};