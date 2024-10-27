import React, { useState, useEffect } from 'react';
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
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';

const Sidebar = ({ setPage }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [userDetails, setUserDetails] = useState(null);
  const [loading, setLoading] = useState(true);

  const navigate = useNavigate();
  
  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  const fetchUserDetails = async () => {
    const userId = localStorage.getItem('user_id');
    
    if (!userId) {
      toast.error("Session expired! Please login again.");
      setTimeout(() => {
        navigate('/auth/login'); 
      }, 3000);
      return;
    }
    
    try {
      const response = await fetch(`http://localhost:8000/users/${userId}`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setUserDetails(data);
    } catch (error) {
      toast.error("Failed to fetch user details. Redirecting to login...");
      setTimeout(() => {
        window.location.href = '/auth/login'; // Redirect to login
      }, 3000);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUserDetails();
  }, []);

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
            <button
              onClick={() => setPage('explorer')} 
              className="flex items-center px-3 py-2 w-full text-base font-medium text-gray-900 rounded-lg hover:bg-gray-100"
            >
              <Compass className="w-4 h-4 mr-3 text-gray-500" />
              Explore
            </button>

            {/* Activity Section */}
            <div className="pt-2">
              <div className="px-3 py-2 text-xs font-semibold text-gray-500 uppercase">
                Activity
              </div>
              <div className="space-y-1">
                <button
                  onClick={() => setPage('liked')}
                  className="flex items-center px-3 py-2 text-base w-full text-gray-700 rounded-lg hover:bg-gray-100"
                >
                  <ThumbsUp className="w-4 h-4 mr-3 text-gray-400" />
                  Liked Articles
                </button>
                <button
                  onClick={() => setPage('disliked')}
                  className="flex items-center px-3 py-2 text-base w-full text-gray-700 rounded-lg hover:bg-gray-100"
                >
                  <ThumbsDown className="w-4 h-4 mr-3 text-gray-400" />
                  Disliked Articles
                </button>
                <button
                  onClick={() => setPage('saved')}
                  className="flex items-center px-3 py-2 text-base w-full  text-gray-700 rounded-lg hover:bg-gray-100"
                >
                  <BookmarkCheck className="w-4 h-4 mr-3 text-gray-400" />
                  Saved Articles
                </button>
              </div>
            </div>

            {/*Chatbot Section*/}
            <div className="pt-2">
              <div className="px-3 py-2 text-xs font-semibold text-gray-500 uppercase">
                Chatbot
              </div>
              <div className="space-y-1">
                <button
                  onClick={() => setPage("chatbot")}
                  className="flex items-center px-3 py-2 text-base w-full text-gray-700 rounded-lg hover:bg-gray-100"
                >
                  <Compass className="
                  w-4 h-4 mr-3 text-gray-400" 
                  />
                  Chatbot
                </button>
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
                  <div className="text-base font-medium text-gray-900">{loading ? "Loading..." : (userDetails ? userDetails.username : "username")}</div>
                </div>
              </div>
              <button 
                onClick={() => alert("Logging out...")} 
                className="flex items-center w-full px-3 py-2 text-base text-red-600 rounded-lg hover:bg-red-50"
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
