export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-center font-mono text-sm">
        <h1 className="text-4xl font-bold mb-4 text-center">
          HRM Platform
        </h1>
        <p className="text-center text-muted-foreground mb-8">
          Система подбора кандидатов и вакансий
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-8">
          <div className="p-6 border rounded-lg hover:border-primary transition-colors">
            <h2 className="text-xl font-semibold mb-2">Для кандидатов</h2>
            <p className="text-muted-foreground">
              Найдите идеальную вакансию на основе ваших навыков и опыта
            </p>
          </div>

          <div className="p-6 border rounded-lg hover:border-primary transition-colors">
            <h2 className="text-xl font-semibold mb-2">Для работодателей</h2>
            <p className="text-muted-foreground">
              Подберите лучших кандидатов с помощью интеллектуального скоринга
            </p>
          </div>
        </div>

        <div className="mt-8 text-center">
          <p className="text-sm text-muted-foreground">
            API Documentation: <a href="http://localhost:8000/docs" className="text-primary hover:underline" target="_blank">http://localhost:8000/docs</a>
          </p>
        </div>
      </div>
    </main>
  )
}
