import { NgModule } from '@angular/core';
import { RouterModule, Routes} from "@angular/router";

import { ListproductsComponent } from "./listproducts/listproducts.component";
import {LoginComponent} from "./login/login.component";
import {CartComponent} from "./cart/cart.component";

const routes: Routes = [
  {path: "", component: ListproductsComponent, data:{source: 'dashboard'}},
  {path: "dashboard", component: ListproductsComponent, data:{source: 'dashboard'}},
  {path: "myproducts", component: ListproductsComponent, data:{source: 'my-products'}},
  {path: "login", component: LoginComponent},
  {path: "cart", component: CartComponent}
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