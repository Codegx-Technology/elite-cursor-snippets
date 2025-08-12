import { useState }s from 'react';
import Card from '@/components/Card';
import Pagination from '@/components/Pagination';

export default function ProjectsPage() {
  const [currentPage, setCurrentPage] = useState(1);
  const totalPages = 5; // Dummy total pages
  const totalItems = 50; // Dummy total items

  const handlePageChange = (page: number) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
    }
  };

  // Dummy project data for demonstration
  const projects = Array.from({ length: 10 }, (_, i) => ({
    id: i + 1 + (currentPage - 1) * 10,
    name: `Project ${i + 1 + (currentPage - 1) * 10}`,
    description: `Description for Project ${i + 1 + (currentPage - 1) * 10}.`,
  }));

  return (
    <Card className="p-6">
      <h1 className="section-title mb-4">Projects</h1>
      <p className="text-soft-text mb-6">Manage your creative projects.</p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        {projects.map((project) => (
          <div key={project.id} className="elite-card p-4">
            <h2 className="font-semibold text-lg mb-2">{project.name}</h2>
            <p className="text-sm text-soft-text">{project.description}</p>
          </div>
        ))}
      </div>

      <Pagination
        currentPage={currentPage}
        totalPages={totalPages}
        totalItems={totalItems}
        onPageChange={handlePageChange}
      />
    </Card>
  );
}