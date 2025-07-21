import { Component } from '@angular/core';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  template: `
    <div class="grid grid-cols-12 gap-8">
      <div class="col-span-12">
        dashboard works!
      </div>
    </div>
  `
})
export class Dashboard {}
