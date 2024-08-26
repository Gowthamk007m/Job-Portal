import React from 'react';
import NavigationPage from '@/components/Navigation';
import DisplayJobs from '@/components/DisplayJobs';
import SearchJobs from '@/components/SearchJobs';
function HomePage(props) {
  return (
    <div>
      <NavigationPage/>
<SearchJobs/>
      <DisplayJobs/>

    </div>
  );
}

export default HomePage;