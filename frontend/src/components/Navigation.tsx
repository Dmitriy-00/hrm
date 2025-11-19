/**
 * Main navigation component
 */
'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Users, Briefcase, TrendingUp, Database, BarChart3 } from 'lucide-react';

const navItems = [
  { href: '/', label: 'Главная', icon: TrendingUp },
  { href: '/dashboard', label: 'Аналитика', icon: BarChart3 },
  { href: '/candidates', label: 'Кандидаты', icon: Users },
  { href: '/vacancies', label: 'Вакансии', icon: Briefcase },
  { href: '/ontology', label: 'Онтология', icon: Database },
];

export function Navigation() {
  const pathname = usePathname();

  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-8">
            <Link href="/" className="flex items-center space-x-2">
              <TrendingUp className="h-6 w-6 text-blue-600" />
              <span className="text-xl font-bold text-gray-900">HRM Platform</span>
            </Link>

            <div className="hidden md:flex space-x-1">
              {navItems.map((item) => {
                const Icon = item.icon;
                const isActive = pathname === item.href;

                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`
                      flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors
                      ${isActive
                        ? 'bg-blue-50 text-blue-700'
                        : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                      }
                    `}
                  >
                    <Icon className="h-4 w-4" />
                    <span>{item.label}</span>
                  </Link>
                );
              })}
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-500">MVP v0.1.0</span>
          </div>
        </div>
      </div>
    </nav>
  );
}
