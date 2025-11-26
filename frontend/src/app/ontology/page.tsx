/**
 * Ontology page - Reference data
 */
'use client';

import { useState } from 'react';
import { useJobTitles, useTechnologies, useStandards, useIndustries } from '@/lib/hooks/useOntology';
import { Database, Code, Award, Building, Loader2, Search } from 'lucide-react';

export default function OntologyPage() {
  const [activeTab, setActiveTab] = useState<'technologies' | 'job-titles' | 'standards' | 'industries'>('technologies');
  const [searchTerm, setSearchTerm] = useState('');

  const { data: jobTitles, isLoading: jobTitlesLoading } = useJobTitles();
  const { data: technologies, isLoading: technologiesLoading } = useTechnologies();
  const { data: standards, isLoading: standardsLoading } = useStandards();
  const { data: industries, isLoading: industriesLoading } = useIndustries();

  const tabs = [
    { id: 'technologies' as const, label: 'Технологии', icon: Code, count: technologies?.length || 0, loading: technologiesLoading },
    { id: 'job-titles' as const, label: 'Должности', icon: Award, count: jobTitles?.length || 0, loading: jobTitlesLoading },
    { id: 'standards' as const, label: 'Стандарты', icon: Database, count: standards?.length || 0, loading: standardsLoading },
    { id: 'industries' as const, label: 'Индустрии', icon: Building, count: industries?.length || 0, loading: industriesLoading },
  ];

  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      language: 'bg-blue-100 text-blue-700',
      framework: 'bg-purple-100 text-purple-700',
      database: 'bg-green-100 text-green-700',
      devops: 'bg-orange-100 text-orange-700',
      cloud: 'bg-cyan-100 text-cyan-700',
      testing: 'bg-pink-100 text-pink-700',
      mobile: 'bg-indigo-100 text-indigo-700',
      data: 'bg-teal-100 text-teal-700',
      ml: 'bg-violet-100 text-violet-700',
      gamedev: 'bg-amber-100 text-amber-700',
    };
    return colors[category] || 'bg-gray-100 text-gray-700';
  };

  const filterItems = <T extends { name: string }>(items: T[] | undefined): T[] => {
    if (!items) return [];
    if (!searchTerm) return items;
    return items.filter(item =>
      item.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Онтология</h1>
        <p className="text-gray-600 mt-1">
          Справочники должностей, технологий, стандартов и индустрий
        </p>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-1 p-2" aria-label="Tabs">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`
                    flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-colors
                    ${isActive
                      ? 'bg-blue-50 text-blue-700'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                    }
                  `}
                >
                  <Icon className="h-4 w-4" />
                  <span>{tab.label}</span>
                  {!tab.loading && (
                    <span className={`px-2 py-0.5 rounded-full text-xs ${isActive ? 'bg-blue-100' : 'bg-gray-100'}`}>
                      {tab.count}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Search */}
        <div className="p-4 border-b border-gray-200">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder={`Поиск ${tabs.find(t => t.id === activeTab)?.label.toLowerCase()}...`}
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        {/* Content */}
        <div className="p-6">
          {/* Technologies */}
          {activeTab === 'technologies' && (
            <div>
              {technologiesLoading ? (
                <div className="flex justify-center py-8">
                  <Loader2 className="h-6 w-6 animate-spin text-blue-600" />
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                  {filterItems(technologies).map((tech) => (
                    <div key={tech.id} className="border border-gray-200 rounded-lg p-4 hover:border-blue-500 transition-colors">
                      <div className="flex items-start justify-between mb-2">
                        <h3 className="font-semibold text-gray-900">{tech.name}</h3>
                        <span className={`px-2 py-1 rounded-md text-xs font-medium ${getCategoryColor(tech.category)}`}>
                          {tech.category}
                        </span>
                      </div>
                      <div className="flex items-center justify-between text-sm text-gray-600">
                        <span>Сложность: {tech.difficulty_level}/5</span>
                        <span>★ {tech.popularity_score}</span>
                      </div>
                      {tech.tags && tech.tags.length > 0 && (
                        <div className="mt-2 flex flex-wrap gap-1">
                          {tech.tags.slice(0, 3).map((tag, idx) => (
                            <span key={idx} className="px-1.5 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">
                              {tag}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Job Titles */}
          {activeTab === 'job-titles' && (
            <div>
              {jobTitlesLoading ? (
                <div className="flex justify-center py-8">
                  <Loader2 className="h-6 w-6 animate-spin text-blue-600" />
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {filterItems(jobTitles).map((title) => (
                    <div key={title.id} className="border border-gray-200 rounded-lg p-4 hover:border-blue-500 transition-colors">
                      <div className="flex items-start justify-between mb-2">
                        <h3 className="font-semibold text-gray-900">{title.name}</h3>
                        <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-md">
                          Level {title.level}
                        </span>
                      </div>
                      {title.description && (
                        <p className="text-sm text-gray-600 line-clamp-2">{title.description}</p>
                      )}
                      {title.aliases && title.aliases.length > 0 && (
                        <div className="mt-2 text-xs text-gray-500">
                          Также: {title.aliases.slice(0, 2).join(', ')}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Standards */}
          {activeTab === 'standards' && (
            <div>
              {standardsLoading ? (
                <div className="flex justify-center py-8">
                  <Loader2 className="h-6 w-6 animate-spin text-blue-600" />
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {filterItems(standards).map((standard) => (
                    <div key={standard.id} className="border border-gray-200 rounded-lg p-4 hover:border-blue-500 transition-colors">
                      <div className="flex items-start justify-between mb-2">
                        <h3 className="font-semibold text-gray-900">{standard.name}</h3>
                        <span className="px-2 py-1 bg-purple-100 text-purple-700 text-xs rounded-md">
                          {standard.category}
                        </span>
                      </div>
                      {standard.description && (
                        <p className="text-sm text-gray-600 line-clamp-2">{standard.description}</p>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Industries */}
          {activeTab === 'industries' && (
            <div>
              {industriesLoading ? (
                <div className="flex justify-center py-8">
                  <Loader2 className="h-6 w-6 animate-spin text-blue-600" />
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {filterItems(industries).map((industry) => (
                    <div key={industry.id} className="border border-gray-200 rounded-lg p-4 hover:border-blue-500 transition-colors">
                      <div className="flex items-start justify-between mb-2">
                        <h3 className="font-semibold text-gray-900">{industry.name}</h3>
                        <span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-md">
                          Level {industry.level}
                        </span>
                      </div>
                      {industry.description && (
                        <p className="text-sm text-gray-600 line-clamp-2">{industry.description}</p>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Empty state */}
          {searchTerm && (
            <>
              {activeTab === 'technologies' && filterItems(technologies).length === 0 && (
                <div className="text-center py-8 text-gray-600">Технологии не найдены</div>
              )}
              {activeTab === 'job-titles' && filterItems(jobTitles).length === 0 && (
                <div className="text-center py-8 text-gray-600">Должности не найдены</div>
              )}
              {activeTab === 'standards' && filterItems(standards).length === 0 && (
                <div className="text-center py-8 text-gray-600">Стандарты не найдены</div>
              )}
              {activeTab === 'industries' && filterItems(industries).length === 0 && (
                <div className="text-center py-8 text-gray-600">Индустрии не найдены</div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
