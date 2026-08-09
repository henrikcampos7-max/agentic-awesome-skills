import { screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { renderWithRouter } from '../../utils/testUtils';
import { GuiaDashboard } from '../GuiaDashboard';

describe('GuiaDashboard', () => {
  it('renders the responsive desktop dashboard structure', () => {
    renderWithRouter(<GuiaDashboard />, { route: '/dashboard-monitor', path: '/dashboard-monitor', useProvider: false });

    expect(screen.getByRole('heading', { level: 1, name: 'MONITOR DE GUIAS - SOLUS' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Sincronizar agora' })).toBeInTheDocument();
    expect(screen.getByRole('heading', { level: 2, name: 'LISTA DE GUIAS' })).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Buscar guia, paciente ou ciência...')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Visualizar guia 01245320' })).toBeInTheDocument();
  });
});
