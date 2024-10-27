import React from 'react'
import logo from '../../logo.png'

function Navbar() {

    return (
        <div>
            <header className="absolute inset-x-0 top-0 z-50">
                <nav aria-label="Global" className="flex items-center justify-between p-6 lg:px-8">
                    <div className="flex lg:flex-1">
                        <a href="#" className="flex gap-2 items-center">
                            <span className="sr-only">Mandrills</span>
                            <img
                                alt=""
                                src={logo}
                                className="h-16 rounded-full w-auto"
                            />
                            <h1 className='text-2xl'>Mandrills</h1>
                        </a>
                    </div>

                </nav>
            </header>
        </div>
    )
}

export default Navbar
