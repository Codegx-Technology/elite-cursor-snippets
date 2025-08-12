import Link from 'next/link';
import { FaHome, FaProjectDiagram, FaCog, FaVideo } from 'react-icons/fa'; // Importing icons

export default function Sidebar({ isSidebarOpen, setSidebarOpen }: { isSidebarOpen: boolean, setSidebarOpen: (isOpen: boolean) => void }) {
  return (
    <aside
      className={`transform ${
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
      } md:translate-x-0 fixed inset-y-0 left-0 z-30 w-64 bg-gray-800 text-white p-4 transition-transform duration-300 ease-in-out`}
    >
      <div className="flex justify-end md:hidden">
        <button
          onClick={() => setSidebarOpen(false)}
          className="text-white focus:outline-none focus:text-gray-300"
        >
          <svg
            className="h-6 w-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M6 18L18 6M6 6l12 12"
            ></path>
          </svg>
        </button>
      </div>
      <nav className="mt-10">
        <ul>
          <li className="mb-2">
            <Link href="/dashboard" className="flex items-center py-2 px-4 rounded hover:bg-gray-700">
              <FaHome className="mr-3" /> Dashboard
            </Link>
          </li>
          <li className="mb-2">
            <Link href="/projects" className="flex items-center py-2 px-4 rounded hover:bg-gray-700">
              <FaProjectDiagram className="mr-3" /> Projects
            </Link>
          </li>
          <li className="mb-2">
            <Link href="/settings" className="flex items-center py-2 px-4 rounded hover:bg-gray-700">
              <FaCog className="mr-3" /> Settings
            </Link>
          </li>
          <li className="mb-2">
            <Link href="/video-generate" className="flex items-center py-2 px-4 rounded hover:bg-gray-700">
              <FaVideo className="mr-3" /> Generate Video
            </Link>
          </li>
        </ul>
      </nav>
    </aside>
  );
}
