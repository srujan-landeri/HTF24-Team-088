import React from 'react'
import Sidebar from '../components/ui/Sidebar'
import Explore from '../components/Explore'
import FeedPage from '../components/CustomFeed'
import UserLikes from '../components/UserLikes'
import UserUnlikes from '../components/UserUnlikes'
import UserSaved from '../components/UserSaved'
import Test from '../components/Test'

function Dashboard() {
  const [page, setPage] = React.useState('')

  return (
    <div>
      <Sidebar setPage={setPage} />
      <Test/>
      {page == "explorer" && <Explore />}
      {page == "feed" && <FeedPage />}
      {page == "liked" && <UserLikes setPage = {setPage}/>}
      {page == "disliked" && <UserUnlikes setPage = {setPage}/>}
      {page == "saved" && <UserSaved setPage = {setPage}/>}
    </div>
  )
}

export default Dashboard
