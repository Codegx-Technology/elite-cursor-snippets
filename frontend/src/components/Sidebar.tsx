export default function Sidebar() {
  return (
    <aside className="w-64 bg-gray-800 text-white p-4">
      <nav>
        <ul>
          <li className="mb-2">
            <a href="#" className="hover:text-gray-300">Dashboard</a>
          </li>
          <li className="mb-2">
            <a href="#" className="hover:text-gray-300">Projects</a>
          </li>
          <li className="mb-2">
            <a href="#" className="hover:text-gray-300">Settings</a>
          </li>
        </ul>
      </nav>
    </aside>
  );
}
