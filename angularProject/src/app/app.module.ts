import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { ListproductsComponent } from './listproducts/listproducts.component';
import {LoginComponent} from './login/login.component';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {LoginService} from "./login.service";
import {HttpClientModule} from "@angular/common/http";
import { MyNavbarComponent } from './my-navbar/my-navbar.component';
import { AppRoutingModule } from './app-routing.module';
import { FilterComponent } from './filter/filter.component';
import { CartComponent } from './cart/cart.component';
import { ProductDetailsComponent } from './product-details/product-details.component';
import { HistorytableComponent } from './historytable/historytable.component';
import { HistoryComponent } from './history/history.component';
import { PaymentformComponent } from './paymentform/paymentform.component';
import { NewProductFormComponent } from './new-product-form/new-product-form.component';


@NgModule({
  declarations: [
    AppComponent,
    ListproductsComponent,
    LoginComponent,
    MyNavbarComponent,
    FilterComponent,
    CartComponent,
    ProductDetailsComponent,
    HistorytableComponent,
    HistoryComponent,
    PaymentformComponent,
    NewProductFormComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    AppRoutingModule
  ],
  providers: [LoginService],
  bootstrap: [AppComponent]
})
export class AppModule {
}
