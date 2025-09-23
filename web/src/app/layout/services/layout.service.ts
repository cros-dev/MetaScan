import { Injectable, signal, effect } from '@angular/core';

export interface LayoutConfig {
  darkTheme?: boolean;
  menuMode?: string;
}

interface LayoutState {
  staticMenuDesktopInactive?: boolean;
  overlayMenuActive?: boolean;
  staticMenuMobileActive?: boolean;
}

@Injectable({ providedIn: 'root' })
export class LayoutService {
  private _config: LayoutConfig = {
    darkTheme: false,
    menuMode: 'static'
  };

  private _state: LayoutState = {
    staticMenuDesktopInactive: false,
    overlayMenuActive: false,
    staticMenuMobileActive: false
  };

  layoutConfig = signal<LayoutConfig>(this._config);
  layoutState = signal<LayoutState>(this._state);

  constructor() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      this.layoutConfig.update(cfg => ({ ...cfg, darkTheme: true }));
    } else if (savedTheme === 'light') {
      this.layoutConfig.update(cfg => ({ ...cfg, darkTheme: false }));
    }

    effect(() => {
      const config = this.layoutConfig();
      if (config) {
        this.toggleDarkMode(config);
      }
    });
  }

  toggleDarkMode(config?: LayoutConfig): void {
    const _config = config || this.layoutConfig();
    if (_config.darkTheme) {
      document.documentElement.classList.add('app-dark');
    } else {
      document.documentElement.classList.remove('app-dark');
    }
  }

  toggleTheme() {
    this.layoutConfig.update(cfg => {
      const newConfig = { ...cfg, darkTheme: !cfg.darkTheme };
      localStorage.setItem('theme', newConfig.darkTheme ? 'dark' : 'light');
      return newConfig;
    });
  }

  isOverlay() {
    return this.layoutConfig().menuMode === 'overlay';
  }

  isDesktop() {
    return window.innerWidth > 991;
  }

  onMenuToggle() {
    if (this.isOverlay()) {
      this.layoutState.update(prev => ({ ...prev, overlayMenuActive: !this.layoutState().overlayMenuActive }));
    }
    if (this.isDesktop()) {
      this.layoutState.update(prev => ({ ...prev, staticMenuDesktopInactive: !this.layoutState().staticMenuDesktopInactive }));
    } else {
      this.layoutState.update(prev => ({ ...prev, staticMenuMobileActive: !this.layoutState().staticMenuMobileActive }));
    }
  }

  collapseMenu() {
    if (this.isOverlay()) {
      this.layoutState.update(prev => ({ ...prev, overlayMenuActive: false }));
    }
    if (this.isDesktop()) {
      this.layoutState.update(prev => ({ ...prev, staticMenuDesktopInactive: true }));
    } else {
      this.layoutState.update(prev => ({ ...prev, staticMenuMobileActive: false }));
    }
  }
}
