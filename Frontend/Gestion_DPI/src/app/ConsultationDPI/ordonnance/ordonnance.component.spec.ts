import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OrdonnanceComponent } from './ordonnance.component';

describe('OrdonnanceComponent', () => {
  let component: OrdonnanceComponent;
  let fixture: ComponentFixture<OrdonnanceComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OrdonnanceComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OrdonnanceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
