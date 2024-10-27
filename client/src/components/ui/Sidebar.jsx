import React, { useState } from 'react';
import { 
  Menu, 
  X, 
  Home, 
  PlusCircle, 
  BookmarkCheck, 
  ThumbsUp, 
  ThumbsDown,
  Compass,
  User,
  LogOut
} from 'lucide-react';

const Sidebar = ({ username }) => {
  const [isOpen, setIsOpen] = useState(false);
  username = "John Doe";
  
  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="relative">
      {/* Sidebar */}
      <aside
        className={`fixed top-0 left-0 z-40 w-56 h-screen transition-transform bg-white border-r border-gray-200 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'}`}
      >
        <div className="flex flex-col h-full py-4">
          {/* Toggle Button - Now attached to the sidebar */}
          <button
            onClick={toggleSidebar}
            className="absolute -right-12 top-4 p-2 bg-white rounded-lg shadow-md hover:bg-gray-100"
          >
            {isOpen ? <X size={24} /> : <Menu size={24} />}
          </button>

          {/* Main Navigation */}
          <nav className="flex-1 px-1">
            {/* Explore Section */}
            <a 
              href="#" 
              className="flex items-center px-3 py-2 text-sm font-medium text-gray-900 rounded-lg hover:bg-gray-100"
            >
              <Compass className="w-4 h-4 mr-3 text-gray-500" />
              Explore
            </a>

            {/* My Feed Section */}
            <div className="pt-2">
              <div className="flex items-center px-3 py-2 text-sm font-medium text-gray-900">
                <Home className="w-4 h-4 mr-3 text-gray-500" />
                My Feed
              </div>
              <a 
                href="#" 
                className="flex items-center px-3 py-2 ml-1 text-sm text-gray-700 rounded-lg hover:bg-gray-100"
              >
                <PlusCircle className="w-4 h-4 mr-2 text-gray-400" />
                Add Feed
              </a>
            </div>

            {/* Activity Section */}
            <div className="pt-2">
              <div className="px-3 py-2 text-xs font-semibold text-gray-500 uppercase">
                Activity
              </div>
              <div className="space-y-1">
                <a 
                  href="#" 
                  className="flex items-center px-3 py-2 text-sm text-gray-700 rounded-lg hover:bg-gray-100"
                >
                  <ThumbsUp className="w-4 h-4 mr-3 text-gray-400" />
                  Liked Articles
                </a>
                <a 
                  href="#" 
                  className="flex items-center px-3 py-2 text-sm text-gray-700 rounded-lg hover:bg-gray-100"
                >
                  <ThumbsDown className="w-4 h-4 mr-3 text-gray-400" />
                  Disliked Articles
                </a>
                <a 
                  href="#" 
                  className="flex items-center px-3 py-2 text-sm text-gray-700 rounded-lg hover:bg-gray-100"
                >
                  <BookmarkCheck className="w-4 h-4 mr-3 text-gray-400" />
                  Saved Articles
                </a>
              </div>
            </div>
          </nav>

          {/* User Profile Section */}
          <div className="px-3 pt-2 mt-2 border-t border-gray-200">
            <div className="px-3 py-2 text-xs font-semibold text-gray-500 uppercase">
              User Profile
            </div>
            <div className="p-3 rounded-lg hover:bg-gray-100">
              <div className="flex items-center mb-3">
                <div className="w-8 h-8 mr-3 rounded-full bg-gray-200 flex items-center justify-center">
                  <User className="w-5 h-5 text-gray-500" />
                </div>
                <div className="flex-1">
                  <div className="text-sm font-medium text-gray-900">{username}</div>
                </div>
              </div>
              <button 
                onClick={() => alert("Logging out...")} 
                className="flex items-center w-full px-3 py-2 text-sm text-red-600 rounded-lg hover:bg-red-50"
              >
                <LogOut className="w-4 h-4 mr-3" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </aside>
    </div>
  );
};

export default Sidebar;