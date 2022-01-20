import { NgModule } from '@angular/core';
import { RouterModule, Routes} from "@angular/router";

import { ListproductsComponent } from "./listproducts/listproducts.component";
import {LoginComponent} from "./login/login.component";

const routes: Routes = [
  {path: "", component: ListproductsComponent, data:{source: 'dashboard'}},
  {path: "dashboard", component: ListproductsComponent, data:{source: 'dashboard'}},
  {path: "myproducts", component: ListproductsComponent, data:{source: 'myproducts'}},
  {path: "login", component: LoginComponent}
];

@NgModule({
  exports: [
    RouterModule
  ],
  imports: [
    RouterModule.forRoot(routes)
  ]
})
export class AppRoutingModule { }
