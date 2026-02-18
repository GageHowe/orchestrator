package main

import (
	"net/http"

	"github.com/labstack/echo/v5"
	"github.com/labstack/echo/v5/middleware"
)

func main() {
	e := echo.New()
	e.Use(middleware.RequestLogger())

	e.GET("/", func(c *echo.Context) error {
		return c.String(http.StatusOK, "200, server is up")
	})
	e.GET("/auth", func(c *echo.Context) error {

		// x := e.AcquireContext().Request()
		// return c.String()
	})

	if err := e.Start(":1323"); err != nil {
		e.Logger.Error("failed to start server", "error", err)
	}
}
