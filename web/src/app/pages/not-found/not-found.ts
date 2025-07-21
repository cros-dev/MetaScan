import { Component } from '@angular/core';

@Component({
  selector: 'app-notfound',
  standalone: true,
  template: `
    <div class="grid grid-cols-12 gap-8">
      <div class="col-span-12">
        <h1>Página não encontrada</h1>
        <p>O endereço acessado não existe.</p>
      </div>
    </div>
  `
})
export class Notfound {} 