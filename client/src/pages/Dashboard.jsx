import React from 'react'
import Sidebar from '../components/ui/Sidebar'
import Explore from '../components/Explore'
import FeedPage from '../components/CustomFeed'
import UserLikes from '../components/UserLikes'
import UserUnlikes from '../components/UserUnlikes'
import UserSaved from '../components/UserSaved'
import Chatbot from '../components/Chatbot'

function Dashboard() {
  const [page, setPage] = React.useState('explorer')

  return (
    <div>
      <Sidebar setPage={setPage} />
      {page == "explorer" && <Explore />}
      {page == "feed" && <FeedPage />}
      {page == "liked" && <UserLikes setPage = {setPage}/>}
      {page == "disliked" && <UserUnlikes setPage = {setPage}/>}
      {page == "saved" && <UserSaved setPage = {setPage}/>}
      {page == "chatbot" && <Chatbot />}
    </div>
  )
}

export default Dashboard
