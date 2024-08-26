import React from "react";
import { ChevronLeftIcon, ChevronRightIcon } from "@heroicons/react/20/solid";

const n = 8;
const DisplayJobs = () => {
  const divArray = Array.from({ length: 10 });
  return (
    <div className="container-fluid bg-gray-900 ">
      <div className="container rounded p-6 bg-gray-700">

        <div className=" col-3 mb-4 text-white ">
          <h3 className="text-2xl">Recommended Jobs</h3>
        </div>

        {divArray.map((_, index) => (
          <div
            key={index}
            className="mb-2 border-2 border-gray-50 bg-slate-50  shadow shadow-slate-50 w-full max-w-8xl flex  flex-col sm:flex-row gap-3 sm:items-center  justify-between px-5 py-4 rounded-md"
          >
            <div>
              <span className="text-purple-800 text-sm">Engineering</span>
              <h3 className="font-bold mt-px">
                Senior Full Stack Backend Engineer
              </h3>
              <div className="flex items-center gap-3 mt-2">
                <span className="bg-purple-100 text-purple-700 rounded-full px-3 py-1 text-sm">
                  Full-time
                </span>
                <span className="text-slate-600 text-sm flex gap-1 items-center">
                  {" "}
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-4 w-4"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={2}
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                    />
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                    />
                  </svg>{" "}
                  Remote, UK
                </span>
              </div>
            </div>
            <div>
              <button className="bg-purple-900 text-white font-medium px-4 py-2 rounded-md flex gap-1 items-center">
                Apply Now{" "}
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-4 w-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M13 7l5 5m0 0l-5 5m5-5H6"
                  />
                </svg>
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DisplayJobs;
