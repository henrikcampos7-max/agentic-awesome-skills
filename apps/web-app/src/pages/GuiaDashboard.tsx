import {
  ArrowsClockwise,
  Bell,
  CalendarBlank,
  ClipboardText,
  ClockCounterClockwise,
  DotsThree,
  Eye,
  FileText,
  FunnelSimple,
  Gear,
  House,
  MagnifyingGlass,
  Plus,
  SquaresFour,
  SignOut,
  WarningCircle,
  X,
} from '@phosphor-icons/react';
import { useMemo } from 'react';
import { usePageMeta } from '../hooks/usePageMeta';
import './guia-dashboard.css';

interface NavItem {
  label: string;
  icon: typeof House;
  active?: boolean;
}

const navItems: ReadonlyArray<NavItem> = [
  { label: 'Dashboard', icon: House, active: true },
  { label: 'Guias', icon: ClipboardText },
  { label: 'Nova Guia', icon: Plus },
  { label: 'Relatórios', icon: FileText },
  { label: 'Alertas', icon: Bell },
  { label: 'Histórico', icon: ClockCounterClockwise },
  { label: 'Configurações', icon: Gear },
];

const metricCards = [
  {
    label: 'Em monitoramento',
    helper: 'Guias ativas',
    value: '32',
    tone: 'primary',
    icon: ClipboardText,
    points: '12,10 42,10 72,16 102,11 132,20 162,9 192,18 222,12',
  },
  {
    label: 'Atualizadas hoje',
    helper: 'Últimas 24h',
    value: '5',
    tone: 'warning',
    icon: Bell,
    points: '12,19 42,18 72,8 102,21 132,12 162,22 192,17 222,19',
  },
  {
    label: 'Pendentes de ciência',
    helper: 'Aguardando ciência',
    value: '7',
    tone: 'danger',
    icon: WarningCircle,
    points: '12,20 42,16 72,23 102,8 132,10 162,19 192,15 222,22',
  },
  {
    label: 'Erros na consulta',
    helper: 'Falhas encontradas',
    value: '1',
    tone: 'neutral',
    icon: X,
    points: '12,22 42,21 72,14 102,20 132,15 162,23 192,19 222,12',
  },
] as const;

const guideRows = [
  {
    number: '01245320',
    patient: 'VALDECIRA LEONES',
    currentStatus: 'Guia emitida / liberada',
    lastCheck: '2026-08-09 04:20:31',
    updatedAt: '2026-08-09 04:20:31',
    science: 'Pendente',
    badge: 'Liberada',
    badgeTone: 'success',
    scienceTone: 'danger',
  },
  {
    number: '11624001',
    patient: 'PEDRO HENRIQUE DA SILVA',
    currentStatus: 'Guia com setor de análise',
    lastCheck: '2026-08-07 02:09:42',
    updatedAt: '2026-08-07 02:09:42',
    science: 'Pendente',
    badge: 'Em análise',
    badgeTone: 'warning',
    scienceTone: 'danger',
  },
  {
    number: '11872533',
    patient: 'MARIA EDUARDA FERREIRA',
    currentStatus: 'Sob auditoria da origem',
    lastCheck: '2026-08-06 10:15:18',
    updatedAt: '2026-08-06 10:15:18',
    science: 'Ciente',
    badge: 'Sob auditoria',
    badgeTone: 'info',
    scienceTone: 'success',
  },
  {
    number: '11003344',
    patient: 'JOÃO CARLOS ALMEIDA',
    currentStatus: 'Guia negada',
    lastCheck: '2026-08-05 16:45:00',
    updatedAt: '2026-08-05 16:45:00',
    science: 'Ciente',
    badge: 'Negada',
    badgeTone: 'danger',
    scienceTone: 'success',
  },
  {
    number: '12567890',
    patient: 'ANA CLARA SOUZA',
    currentStatus: 'Aguardando liberação',
    lastCheck: '2026-08-04 11:30:12',
    updatedAt: '2026-08-04 11:30:12',
    science: 'Pendente',
    badge: 'Pendente',
    badgeTone: 'neutral',
    scienceTone: 'danger',
  },
  {
    number: '11556677',
    patient: 'LUCAS MARTINS COSTA',
    currentStatus: 'Sob auditoria da Unimed Local',
    lastCheck: '2026-08-03 09:12:55',
    updatedAt: '2026-08-03 09:12:55',
    science: 'Pendente',
    badge: 'Sob auditoria',
    badgeTone: 'info',
    scienceTone: 'danger',
  },
] as const;

function sparkLine(points: string, tone: string): React.ReactElement {
  return (
    <svg viewBox="0 0 234 32" role="presentation" aria-hidden="true">
      <polyline className={`guide-dashboard__sparkline guide-dashboard__sparkline--${tone}`} points={points} />
    </svg>
  );
}

export function GuiaDashboard(): React.ReactElement {
  usePageMeta(useMemo(() => ({
    title: 'Monitor de Guias - Solus | Agentic Awesome Skills',
    description: 'Dashboard desktop responsivo em HTML e CSS para monitoramento de guias.',
    canonicalPath: '/dashboard-monitor',
  }), []));

  return (
    <div className="guide-dashboard-page">
      <div className="guide-dashboard__window-bar" aria-hidden="true">
        <span />
        <span />
        <span />
      </div>

      <div className="guide-dashboard">
        <aside className="guide-dashboard__sidebar" aria-label="Navegação lateral">
          <div className="guide-dashboard__brand">
            <div className="guide-dashboard__brand-mark">U</div>
            <div>
              <strong>Unimed</strong>
              <span>Centro Rondônia</span>
            </div>
          </div>

          <nav className="guide-dashboard__nav">
            {navItems.map(({ label, icon: ItemIcon, active = false }) => (
              <button key={label} type="button" className={active ? 'is-active' : ''} aria-current={active ? 'page' : undefined}>
                <ItemIcon size={18} weight={active ? 'fill' : 'regular'} />
                <span>{label}</span>
              </button>
            ))}
          </nav>

          <div className="guide-dashboard__profile">
            <div className="guide-dashboard__avatar">HC</div>
            <div>
              <strong>Henrique Campos</strong>
              <span>Farmacêutico</span>
            </div>
          </div>

          <button type="button" className="guide-dashboard__logout">
            <SignOut size={18} />
            <span>Sair</span>
          </button>
        </aside>

        <main className="guide-dashboard__main">
          <section className="guide-dashboard__panel">
            <header className="guide-dashboard__hero">
              <div className="guide-dashboard__hero-copy">
                <p className="guide-dashboard__eyebrow">Monitor de Guias</p>
                <h1>MONITOR DE GUIAS - SOLUS</h1>
                <p>Acompanhe suas guias em tempo real</p>
                <button type="button" className="guide-dashboard__primary-action">
                  <Plus size={18} weight="bold" />
                  <span>Nova Guia</span>
                </button>
              </div>

              <div className="guide-dashboard__hero-actions">
                <div className="guide-dashboard__sync">
                  <div>
                    <ArrowsClockwise size={18} className="guide-dashboard__sync-icon" />
                    <span>Sincronização: 00:20:55</span>
                  </div>
                  <strong>Ativo</strong>
                </div>
                <button type="button" className="guide-dashboard__sync-button">
                  <ArrowsClockwise size={18} />
                  <span>Sincronizar agora</span>
                </button>
                <button type="button" className="guide-dashboard__ghost-icon" aria-label="Mais opções">
                  <DotsThree size={20} weight="bold" />
                </button>
              </div>
            </header>

            <section className="guide-dashboard__section" aria-labelledby="indicators-title">
              <div className="guide-dashboard__section-title">
                <h2 id="indicators-title">INDICADORES</h2>
              </div>

              <div className="guide-dashboard__metrics">
                {metricCards.map(({ label, helper, value, tone, icon: MetricIcon, points }) => (
                  <article key={label} className="guide-dashboard__metric-card">
                    <div className="guide-dashboard__metric-top">
                      <div className={`guide-dashboard__metric-icon guide-dashboard__metric-icon--${tone}`}>
                        <MetricIcon size={24} />
                      </div>
                      <div>
                        <h3>{label}</h3>
                        <p>{helper}</p>
                      </div>
                    </div>
                    <strong className={`guide-dashboard__metric-value guide-dashboard__metric-value--${tone}`}>{value}</strong>
                    {sparkLine(points, tone)}
                  </article>
                ))}
              </div>
            </section>

            <section className="guide-dashboard__section" aria-labelledby="filters-title">
              <div className="guide-dashboard__section-title">
                <h2 id="filters-title">FILTROS</h2>
              </div>

              <div className="guide-dashboard__filters">
                <label>
                  <span>Status:</span>
                  <select defaultValue="Todos">
                    <option>Todos</option>
                    <option>Liberada</option>
                    <option>Em análise</option>
                    <option>Pendente</option>
                  </select>
                </label>

                <label>
                  <span>Período:</span>
                  <div className="guide-dashboard__date-range">
                    <div className="guide-dashboard__date-input">
                      <input type="text" defaultValue="10/07/2026" aria-label="Data inicial" />
                      <CalendarBlank size={18} />
                    </div>
                    <small>até</small>
                    <div className="guide-dashboard__date-input">
                      <input type="text" defaultValue="09/08/2026" aria-label="Data final" />
                      <CalendarBlank size={18} />
                    </div>
                  </div>
                </label>

                <button type="button" className="guide-dashboard__filter-button">
                  <FunnelSimple size={18} />
                  <span>Aplicar filtros</span>
                </button>
              </div>

              <div className="guide-dashboard__toggles">
                <label><input type="checkbox" /> Somente atualizadas hoje</label>
                <label><input type="checkbox" /> Somente pendentes de ciência</label>
                <button type="button" className="guide-dashboard__clear-button">Limpar filtro</button>
              </div>
            </section>

            <section className="guide-dashboard__section guide-dashboard__table-section" aria-labelledby="guides-title">
              <div className="guide-dashboard__table-header">
                <h2 id="guides-title">LISTA DE GUIAS</h2>
                <div className="guide-dashboard__table-tools">
                  <label className="guide-dashboard__search">
                    <MagnifyingGlass size={18} />
                    <input type="search" placeholder="Buscar guia, paciente ou ciência..." />
                  </label>
                  <button type="button" className="guide-dashboard__ghost-icon" aria-label="Alternar visualização">
                    <SquaresFour size={18} />
                  </button>
                </div>
              </div>

              <div className="guide-dashboard__table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Status</th>
                      <th>Número da Guia</th>
                      <th>Nome do Paciente</th>
                      <th>Status Atual</th>
                      <th>Última Consulta</th>
                      <th>Última Alteração</th>
                      <th>Ciência</th>
                      <th>Ações</th>
                    </tr>
                  </thead>
                  <tbody>
                    {guideRows.map((row, index) => (
                      <tr key={`${row.number}-${row.patient}`}>
                        <td>{index + 1}</td>
                        <td><span className={`guide-dashboard__badge guide-dashboard__badge--${row.badgeTone}`}>{row.badge}</span></td>
                        <td>{row.number}</td>
                        <td>{row.patient}</td>
                        <td>{row.currentStatus}</td>
                        <td>{row.lastCheck}</td>
                        <td>{row.updatedAt}</td>
                        <td>
                          <span className={`guide-dashboard__science guide-dashboard__science--${row.scienceTone}`}>
                            <span />
                            {row.science}
                          </span>
                        </td>
                        <td>
                          <div className="guide-dashboard__row-actions">
                            <button type="button" aria-label={`Visualizar guia ${row.number}`}>
                              <Eye size={18} />
                            </button>
                            <button type="button" aria-label={`Mais ações da guia ${row.number}`}>
                              <DotsThree size={18} weight="bold" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <footer className="guide-dashboard__table-footer">
                <p>Exibindo {guideRows.length} registros</p>
                <div className="guide-dashboard__pagination">
                  <label>
                    <span className="sr-only">Itens por página</span>
                    <select defaultValue="10 por página">
                      <option>10 por página</option>
                      <option>20 por página</option>
                      <option>50 por página</option>
                    </select>
                  </label>
                  <div>
                    <button type="button" aria-label="Página anterior">‹</button>
                    <button type="button" className="is-active">1</button>
                    <button type="button">2</button>
                    <button type="button" aria-label="Próxima página">›</button>
                  </div>
                </div>
              </footer>
            </section>

            <footer className="guide-dashboard__app-footer">
              <span>Monitor de Guias - Solus</span>
              <span>v1.1.0 | by henrique.campos</span>
            </footer>
          </section>
        </main>
      </div>
    </div>
  );
}

export default GuiaDashboard;
