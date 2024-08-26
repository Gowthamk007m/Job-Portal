import { Button } from '@headlessui/react'
import React from 'react'

const SearchJobs = () => {
  return (
    <section className="bg-gray-900 text-white py-20">
    <div className="container mx-auto px-4">
      <div className="text-center mb-10">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          Find Your Dream Job
        </h1>
        <p className="text-lg md:text-xl">
          Search among thousands of job listings and apply now
        </p>
      </div>
      {/* Search Form */}
      <div className="max-w-8xl mx-auto">
        <form className="bg-gray-800 rounded-lg p-6 shadow-md">
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-3 gap-3">
            {/* Job Title */}
            <div>
              <label
                htmlFor="job-title"
                className="block ml-1 text-white font-semibold"
              >
                Job Title
              </label>
              <input
                type="text"
                id="job-title"
                className="w-full px-4 py-2 border rounded-lg text-black focus:border-blue-500"
                placeholder="e.g., Software Engineer"
              />
            </div>
            {/* Location */}
            <div>
              <label
                htmlFor="location"
                className="block text-white font-semibold"
              >
                Location
              </label>
              <input
                type="text"
                id="location"
                className="w-full px-4 py-2 text-black border rounded-lg focus:border-blue-500 "
                placeholder="e.g., New York, NY"
              />
            </div>
            {/* Job Type
            <div>
              <label
                htmlFor="job-type"
                className="block text-gray-700 font-semibold"
              >
                Job Type
              </label>
              <select
                id="job-type"
                className="w-full px-4 py-2 border rounded-lg focus:outline-none"
              >
                <option value="">Select Type</option>
                <option value="full-time">Full-Time</option>
                <option value="part-time">Part-Time</option>
                <option value="contract">Contract</option>
                <option value="internship">Internship</option>
              </select>
            </div> */}

            {/* Search */}
            <div className=" mt-6   text-center">
            <Button
              type="submit"
              className="bg-gray-900  hover:bg-blue-700 text-white font-bold py-2 px-20 rounded-lg"
            >
              Search Jobs
            </Button>
            
          </div>
          </div>
     
        </form>
      </div>
    </div>
  </section>
  )
}

export default SearchJobs